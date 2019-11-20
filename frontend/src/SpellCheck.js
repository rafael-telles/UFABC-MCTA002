/* eslint-disable no-console */
/* eslint-disable no-unused-vars */
import { Extension, Plugin } from "tiptap";
import { Decoration, DecorationSet } from "prosemirror-view";
import _ from "lodash";
import Popper from "popper.js";
import Axios from "axios";

export default class SpellCheck extends Extension {
  constructor(options = {}) {
    super(options);

    this.results = [];
    this._updating = false;

    this.checkableWords = new Set();
    this.ignoredWords = new Set();
    this.suggestions = {};
    this.currentSuggestions = {};

    this.popper = null;

    this.apiBase = options.apiBase;
  }

  get name() {
    return "spellcheck";
  }

  init() {
    const self = this;

    const debouncedCheck = _.debounce(function(state) {
      self.check(state);
    }, 500);
    this.editor.on("transaction", ({ state }) => {
      debouncedCheck(state);
    });
  }

  async check(state) {
    const { doc } = state;
    const newCheckableWords = this.findCheckableWords(doc);

    const newWords = _.difference(
      [...newCheckableWords],
      [...this.checkableWords]
    );
    if (newWords.length > 0) {
      const newSuggestions = await this.fetchSuggestions(newWords);
      _.merge(this.suggestions, newSuggestions);
    }

    this.suggestions = _.omit(this.suggestions, [...this.ignoredWords]);
    this.checkableWords = newCheckableWords;

    this.decorateWords(doc, _.keys(this.suggestions));

    this.triggerUpdate();
  }

  async fetchSuggestions(words) {
    const res = await Axios.post(`${this.apiBase}/suggestions`, { words });
    return res.data;
  }

  decorateWords(doc, words) {
    const findRegExp = RegExp(
      words.map(word => `\\b${word}\\b`).join("|"),
      "gui"
    );

    const mergedTextNodes = [];
    let index = 0;

    doc.descendants((node, pos) => {
      if (node.isText) {
        if (mergedTextNodes[index]) {
          mergedTextNodes[index] = {
            text: mergedTextNodes[index].text + node.text,
            pos: mergedTextNodes[index].pos
          };
        } else {
          mergedTextNodes[index] = {
            text: node.text,
            pos
          };
        }
      } else {
        index += 1;
      }
    });

    this.results = [];
    mergedTextNodes.forEach(({ text, pos }) => {
      const search = findRegExp;
      let m;
      // eslint-disable-next-line no-cond-assign
      while ((m = search.exec(text))) {
        if (m[0] === "") {
          break;
        }

        this.results.push({
          from: pos + m.index,
          to: pos + m.index + m[0].length,
          word: m[0].toLowerCase()
        });
      }
    });
  }

  findCheckableWords(doc) {
    const mergedTextNodes = [];
    let index = 0;

    doc.descendants((node, pos) => {
      if (node.isText) {
        if (mergedTextNodes[index]) {
          mergedTextNodes[index] = {
            text: mergedTextNodes[index].text + node.text,
            pos: mergedTextNodes[index].pos
          };
        } else {
          mergedTextNodes[index] = {
            text: node.text,
            pos
          };
        }
      } else {
        index += 1;
      }
    });

    const checkableWords = mergedTextNodes
      .filter(node => !!node)
      .map(node => node.text.split(/[^\w\d]+/))
      .flat()
      .map(word => word.toLowerCase())
      .filter(word => /^[a-z]+$/.test(word))
      .reduce((set, word) => set.add(word), new Set());

    for (const word of this.ignoredWords) {
      checkableWords.delete(word);
    }
    return checkableWords;
  }

  get decorations() {
    let i = 0;
    return this.results.map(deco =>
      Decoration.inline(deco.from, deco.to, {
        class: "misspelled",
        "data-misspelled-word": deco.word,
        "data-index": i++,
        "data-from": deco.from,
        "data-to": deco.to
      })
    );
  }

  ignore() {
    if (!this.selectedNode) return;

    const word = this.selectedNode.getAttribute("data-misspelled-word");
    this.ignoredWords.add(word);

    const { view } = this.editor;
    this.check(view.state);

    this.triggerUpdate();
  }

  replaceWith(word) {
    if (!this.selectedNode) return;

    const { view } = this.editor;

    const from = +this.selectedNode.getAttribute("data-from");
    const to = +this.selectedNode.getAttribute("data-to");
    const index = +this.selectedNode.getAttribute("data-index");

    this.results.splice(index, 1);
    view.dispatch(view.state.tr.insertText(word, from, to));

    this.triggerUpdate();
  }

  triggerUpdate() {
    const { view } = this.editor;

    setTimeout(function() {
      view.dispatch(view.state.tr);
    }, 100);
  }

  createDeco(doc) {
    const self = this;

    const decorations = this.decorations
      ? DecorationSet.create(doc, this.decorations)
      : [];

    setTimeout(function() {
      const nodes = document.querySelectorAll(`.misspelled`);
      for (let node of nodes) {
        node.oncontextmenu = function(event) {
          event.preventDefault();
          const word = node.getAttribute("data-misspelled-word");
          self.currentSuggestions = self.suggestions[word];

          if (self.popper) self.popper.destroy();

          const el = document.querySelector("#spellcheck-suggestions");
          self.popper = new Popper(node, el);
          self.selectedNode = node;
        };
      }
      document.body.onclick = function() {
        if (self.popper) self.popper.destroy();
        self.currentSuggestions = {};
        self.selectedNode = null;
      };
    }, 0);
    return decorations;
  }

  get plugins() {
    return [
      new Plugin({
        state: {
          init() {
            return DecorationSet.empty;
          },
          apply: (tr, old) => {
            if (tr.docChanged) {
              return old.map(tr.mapping, tr.doc)
            }
            return this.createDeco(tr.doc)
          }
        },
        props: {
          decorations(state) {
            return this.getState(state);
          }
        }
      })
    ];
  }
}
