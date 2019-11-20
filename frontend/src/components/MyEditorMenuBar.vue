<template>
  <editor-menu-bar
    :editor="editor"
    v-slot="{ commands, isActive }"
    class="editor-menu-bar"
  >
    <div class="editor-menu-bar-inner">
      <div class="buttons">
        <button
          :class="{ 'is-active': isActive.bold() }"
          @click="commands.bold"
        >
          <mdi-format-bold />
        </button>

        <button
          :class="{ 'is-active': isActive.italic() }"
          @click="commands.italic"
        >
          <mdi-format-italic />
        </button>

        <button
          :class="{ 'is-active': isActive.strike() }"
          @click="commands.strike"
        >
          <mdi-format-strike-through />
        </button>

        <button
          :class="{ 'is-active': isActive.underline() }"
          @click="commands.underline"
        >
          <mdi-format-underline />
        </button>

        <button
          :class="{ 'is-active': isActive.code() }"
          @click="commands.code"
        >
          <mdi-code-tags />
        </button>

        <button
          :class="{ 'is-active': isActive.paragraph() }"
          @click="commands.paragraph"
        >
          <mdi-format-paragraph />
        </button>

        <button
          :class="{ 'is-active': isActive.heading({ level: 1 }) }"
          @click="commands.heading({ level: 1 })"
        >
          <mdi-format-header-1 />
        </button>

        <button
          :class="{ 'is-active': isActive.heading({ level: 2 }) }"
          @click="commands.heading({ level: 2 })"
        >
          <mdi-format-header-2 />
        </button>

        <button
          :class="{ 'is-active': isActive.heading({ level: 3 }) }"
          @click="commands.heading({ level: 3 })"
        >
          <mdi-format-header-3 />
        </button>

        <button
          :class="{ 'is-active': isActive.bullet_list() }"
          @click="commands.bullet_list"
        >
          <mdi-format-list-bulleted />
        </button>

        <button
          :class="{ 'is-active': isActive.ordered_list() }"
          @click="commands.ordered_list"
        >
          <mdi-format-list-numbered />
        </button>

        <button
          :class="{ 'is-active': isActive.blockquote() }"
          @click="commands.blockquote"
        >
          <mdi-format-quote-close />
        </button>

        <button @click="commands.undo">
          <mdi-undo />
        </button>

        <button @click="commands.redo">
          <mdi-redo />
        </button>
      </div>
      <div style="display: flex; flex: 1 1 auto"></div>
      <div style="display: flex; flex-direction: row;">
        <el-input
          placeholder="Please input"
          v-model="dApiBase"
          size="small"
          style="width: 300px"
        >
          <template slot="prepend">API: </template>
        </el-input>
      </div>
    </div>
  </editor-menu-bar>
</template>

<script>
/* eslint-disable no-console */

import { EditorMenuBar } from "tiptap";

export default {
  name: "MyEditorMenuBar",
  components: {
    EditorMenuBar
  },
  props: {
    editor: Object,
    apiBase: String
  },
  data() {
    return {
      dApiBase: this.apiBase
    };
  },
  watch: {
    dApiBase(val) {
      this.$emit("apiBaseChanged", val);
    }
  }
};
</script>

<style>
.editor-menu-bar {
  height: 32px;
  position: fixed;
  z-index: 1000;
  background: white;
  width: 100%;
  top: 0;
  left: 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.editor-menu-bar-inner {
  display: flex;
  flex: 1 1 auto;
  flex-direction: row;
}
.editor-menu-bar button {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  margin: 0 4px;
  border-radius: 50%;
  transition: 0.3s background;
}
.editor-menu-bar button:hover {
  background: rgba(0, 0, 0, 0.1);
}
.editor-menu-bar button.is-active {
  background: rgba(0, 0, 0, 0.2);
}
.editor-menu-bar button.is-active:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>
