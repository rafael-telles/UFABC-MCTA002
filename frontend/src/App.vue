<template>
  <div class="editor">
    <MyEditorMenuBar :editor="editor" :apiBase="apiBase" @apiBaseChanged="apiBaseChanged"/>

    <editor-content
      class="editor__content"
      :editor="editor"
      :spellcheck="false"
    />
    <div>
      <div id="spellcheck-suggestions" v-show="spellCheck.selectedNode">
        <span>Substituir por:</span>
        <ul>
          <li v-for="(freq, word) in spellCheck.currentSuggestions" :key="word">
            <button @click="spellCheck.replaceWith(word)">{{ word }}</button>
          </li>
        </ul>
        <hr>
        <button @click="spellCheck.ignore()">Ignorar</button>
      </div>
    </div>
  </div>
</template>

<script>
import { Editor, EditorContent } from "tiptap";
import {
  Blockquote,
  CodeBlock,
  Heading,
  HorizontalRule,
  OrderedList,
  BulletList,
  ListItem,
  Bold,
  Code,
  Italic,
  Link,
  Strike,
  Underline,
  History
} from "tiptap-extensions";
import SpellCheck from "./SpellCheck";

import MyEditorMenuBar from "./components/MyEditorMenuBar";

import content from "raw-loader!./sample.html";

export default {
  components: {
    EditorContent,
    MyEditorMenuBar
  },
  data() {
    const apiBase = 'http://localhost:5000/api'
    const spellCheck = new SpellCheck({ apiBase });
    return {
      apiBase,
      spellCheck,
      editor: new Editor({
        extensions: [
          new Blockquote(),
          new BulletList(),
          new CodeBlock(),
          new Heading({ levels: [1, 2, 3] }),
          new HorizontalRule(),
          new ListItem(),
          new OrderedList(),
          new Link(),
          new Bold(),
          new Code(),
          new Italic(),
          new Strike(),
          new Underline(),
          new History(),
          spellCheck
        ],
        content: content
      })
    };
  },
  watch: {
    apiBase(val) {
      this.spellCheck.apiBase = val
    }
  },
  methods: {
    apiBaseChanged(val) {
      this.apiBase = val
    }
  },
  created() {
    window.App = this
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>

<style>
body {
  margin: 0;
}
.editor__content .ProseMirror {
  padding: 32px 12px 0;
  min-height: calc(100vh - 32px - 16px);
}
.editor__content .ProseMirror-focused {
  outline: none;
}
.misspelled {
  border-bottom: 2px dashed red !important;
}

#spellcheck-suggestions {
  background: white;
  border-radius: 6px;
  padding: 8px 14px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc;
}
#spellcheck-suggestions button {
  background: transparent;
  border: 0;
  font-weight: bold;
}

#spellcheck-suggestions ul {
  padding: 0 20px 0 0;
}
</style>
