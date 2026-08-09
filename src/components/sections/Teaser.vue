<script lang="ts" setup>

// 首屏大图：论文 Figure 1，展示 intent jailbreak 与 behavior jailbreak 的差别
const teaser = './images/Figure_1_1.png'

const caption =
  'Intent jailbreaks vs. behavior jailbreaks. Benign scenario: the LLM-based robot generates effective policies for benign instructions while refusing direct harmful queries. Attack scenarios: an intent jailbreak bypasses the refusal mechanism but yields non-executable policies, because it neglects robot-specific syntax constraints and physical feasibility. In contrast, a behavior jailbreak such as POEF induces effective policies that result in actual physical damage.'

</script>

<template>
  <div>
    <el-row justify="center">
      <el-col :xs="24" :sm="24" :md="22" :lg="20" :xl="18">
        <el-image class="teaser" :src="teaser" fit="contain" :preview-src-list="[teaser]" hide-on-click-modal />
      </el-col>
    </el-row>

    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="12">
        <p class="caption">{{ caption }}</p>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>

/* 首屏大图 */
.teaser {
  width: 100%;
  margin-top: 20px;
  border-radius: 10px;
  cursor: zoom-in;
}

/* 图注 */
.caption {
  font-size: 14px;
  line-height: 1.6rem;
  color: var(--el-text-color-secondary);
  text-align: justify;
  margin: 12px 20px 0px 20px;
}

</style>
