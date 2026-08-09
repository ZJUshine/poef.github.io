<script>
export default {
  data() {
    return {
      // NDSS 2027 的正式条目出来之后，把下面的 arXiv 条目换掉
      bibtex: [
        "@misc{lu2025poexpolicyexecutablejailbreak,",
        "    title={POEX: Towards Policy Executable Jailbreak Attacks Against the LLM-based Robots},",
        "    author={Xuancun Lu and Zhengxian Huang and Xinfeng Li and Chi Zhang and Xiaoyu Ji and Wenyuan Xu},",
        "    year={2025},",
        "    eprint={2412.16633},",
        "    archivePrefix={arXiv},",
        "    primaryClass={cs.RO},",
        "    url={https://arxiv.org/abs/2412.16633},",
        "}",
      ],
    }
  },
  methods: {
    copyVal() {
      let oInput = document.createElement('textarea');
      let text = document.getElementById('bibtex').innerText;
      oInput.value = text;
      document.body.appendChild(oInput);
      oInput.select();
      document.execCommand('Copy');
      this.$message.success('Copy Successfully');
      oInput.remove();
    }
  }
}

</script>

<template>
  <div>
    <el-divider />
      
      <el-row justify="center">
        <h1 class="section-title">BibTeX</h1>
      </el-row>
      
      <el-row justify="center">
        <el-col class='bibtex' :xs="24" :sm="20" :md="14" :lg="12" :xl="12" @click="copyVal()" >
          <div style="text-align: center; color: var(--el-text-color-secondary); margin-top: 20px;">🖱️ Click here to copy BibTex.</div> 
          <el-row>
              <el-scrollbar style="margin: 0px 20px 5px 20px;">
                <pre id="bibtex"><code v-for="b in bibtex">{{ b }}<br/></code></pre>
              </el-scrollbar>
          </el-row>
        </el-col>
      </el-row>

  </div>
</template>

<style scoped>

.scrollbar-flex-content {
  display: flex;
}

/* 卡片属性 */
.bibtex {
  margin: 20px 0px;
  padding-top: 5px;
  box-shadow: var(--el-box-shadow-light); 
  border-radius: 10px;
}

/* 卡片悬浮 */
.bibtex:hover {
  box-shadow: var(--el-box-shadow); 
}

/* 卡片点击 */
.bibtex:active{
  box-shadow: var(--el-box-shadow-lighter); 
}

pre {
  border: none;
  border-radius: 0px;
  padding: 10px;
  background: none;
}

pre code {
  font-size: 15px;
  background: #ffffff;
}

/* 窄屏下缩小字号，避免长行被卡片裁掉 */
@media (max-width: 768px) {
  pre code {
    font-size: 12px;
  }
}



</style>