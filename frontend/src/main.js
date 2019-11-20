import Vue from 'vue'
import App from './App.vue'

import ElementUI from 'element-ui'

import './styles.scss'
import 'vue-material-design-icons/styles.css';

import FormatBold from 'vue-material-design-icons/FormatBold.vue';
Vue.component('mdi-format-bold', FormatBold);
import FormatItalic from 'vue-material-design-icons/FormatItalic.vue';
Vue.component('mdi-format-italic', FormatItalic);
import FormatStrikethrough from 'vue-material-design-icons/FormatStrikethrough.vue';
Vue.component('mdi-format-strike-through', FormatStrikethrough);
import FormatUnderline from 'vue-material-design-icons/FormatUnderline.vue';
Vue.component('mdi-format-underline', FormatUnderline);
import CodeTags from 'vue-material-design-icons/CodeTags.vue';
Vue.component('mdi-code-tags', CodeTags);
import FormatParagraph from 'vue-material-design-icons/FormatParagraph.vue';
Vue.component('mdi-format-paragraph', FormatParagraph);
import FormatHeader1 from 'vue-material-design-icons/FormatHeader1.vue';
Vue.component('mdi-format-header-1', FormatHeader1);
import FormatHeader2 from 'vue-material-design-icons/FormatHeader2.vue';
Vue.component('mdi-format-header-2', FormatHeader2);
import FormatHeader3 from 'vue-material-design-icons/FormatHeader3.vue';
Vue.component('mdi-format-header-3', FormatHeader3);
import FormatListBulleted from 'vue-material-design-icons/FormatListBulleted.vue';
Vue.component('mdi-format-list-bulleted', FormatListBulleted);
import FormatListNumbered from 'vue-material-design-icons/FormatListNumbered.vue';
Vue.component('mdi-format-list-numbered', FormatListNumbered);
import FormatQuoteClose from 'vue-material-design-icons/FormatQuoteClose.vue';
Vue.component('mdi-format-quote-close', FormatQuoteClose);


import Undo from 'vue-material-design-icons/Undo.vue';
Vue.component('mdi-undo', Undo);
import Redo from 'vue-material-design-icons/Redo.vue';
Vue.component('mdi-redo', Redo);

Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
