<script>
import Title from './sections/Title.vue'
import Teaser from './sections/Teaser.vue'
import Abstract from './sections/Abstract.vue'
import Dataset from './sections/Dataset.vue'
import Markdown from './sections/Markdown.vue'
import BibTeX from './sections/BibTeX.vue'
import Carousel from './sections/Carousel.vue'
import Video from './sections/Video.vue'
import Echart from './sections/Echart.vue'
import Table from './sections/Table.vue'
import AssetBrowser from './sections/AssetBrowser.vue'
// 评论区默认关闭：模板自带的 Twikoo 后端是模板作者的 Vercel 实例，
// 留言会写进对方的数据库。要启用请先在 Comment.vue 里换成自己的 envId，
// 再把下面的 import 和模板里的 <Comment/> 取消注释。
// import Comment from './sections/Comment.vue'

export default {
  components: {
    Title,
    Teaser,
    Abstract,
    Dataset,
    Markdown,
    BibTeX,
    Carousel,
    Video,
    Echart,
    Table,
    AssetBrowser,
    // Comment,
  }
}
</script>

<template>
  <Title/>
  <Teaser/>
  <Abstract/>
  <Dataset/>
  <Echart/>
  <Markdown/>
  <Table/>
  <Carousel/>
  <Video/>
  <AssetBrowser/>
  <BibTeX/>
  <!-- <Comment/> -->
</template>
