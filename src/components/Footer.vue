<script lang="ts" setup>
// 页脚需要的链接
const links = {
    Nerfies: "https://github.com/nerfies/nerfies.github.io",
    Vue: "https://cn.vuejs.org/",
    Vite: "https://cn.vitejs.dev/",
    ElementPlus: "https://element-plus.org/zh-CN/",
    template: "https://github.com/JunyaoHu/academic-project-page-template-vue",
    repo: "https://github.com/ZJUshine/poef.github.io",
}
</script>

<template>

  <div class="bg">

    <el-watermark :content="['POEF', 'NDSS 2027']" :gap="['60','0']" :z-index="0">
      <el-row justify="center">
        <p class="footer">
          <b>POEF</b> — <i>Easier Said Than Done: Unpacking Intent–Behavior Gap in Jailbreaking LLM-based Robots</i>.<br/>

          Built from the <a :href="links.template">academic project page template</a>, inspired by
          <a :href="links.Nerfies">Nerfies</a>, powered by
          <a :href="links.Vue">Vue</a>,
          <a :href="links.Vite">Vite</a>, and
          <a :href="links.ElementPlus">Element Plus</a>.
        </p>
      </el-row>
    </el-watermark>
  </div>
</template>

<style scoped>

/* 页脚背景 */
.bg {
  background-color: rgb(235, 235, 235);
}

/* 页脚文字 */
.footer {
  text-align: center;
  margin: 20px;
  z-index: 1;
}

</style>
