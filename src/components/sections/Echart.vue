<script>

import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { provide } from 'vue';

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

// 论文 Table II：传统 LLM 越狱攻击在机器人场景下的 IJSR 与 BJSR
// 每一项都是 [IJSR, BJSR]，两者之差即 intent-behavior gap
const models = ['GPT-4-Turbo', 'GPT-3.5-Turbo', 'Yi-1.5-9B', 'Ministral-8B', 'Qwen-2.5-7B']

const attacks = {
  GCG:        { ijsr: [10.00, 43.33, 96.00, 99.33, 80.00], bjsr: [8.00, 0.00, 52.67, 54.67, 54.67] },
  GPTFUZZER:  { ijsr: [17.81, 20.95, 31.71, 26.00, 31.71], bjsr: [11.71, 17.14, 4.29, 0.47, 0.19] },
  TAP:        { ijsr: [14.00, 20.00, 35.33, 35.33, 74.00], bjsr: [8.67, 12.00, 8.00, 13.33, 33.33] },
}

const makeOption = (name) => {
  const a = attacks[name]
  return {
    title: {
      text: `${name}: intent vs. behavior jailbreak`,
      left: 'center',
      textStyle: { fontSize: 15 },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      valueFormatter: (v) => `${Number(v).toFixed(2)}%`,
    },
    legend: { bottom: 0 },
    grid: { left: 50, right: 20, top: 50, bottom: 50 },
    xAxis: {
      type: 'category',
      data: models,
      axisLabel: { interval: 0, rotate: 20, fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      max: 100,
      name: '%',
      nameTextStyle: { padding: [0, 0, 0, 30] },
    },
    series: [
      {
        name: 'IJSR (intent jailbreak)',
        type: 'bar',
        data: a.ijsr,
        itemStyle: { color: '#f0a04b' },
      },
      {
        name: 'BJSR (behavior jailbreak)',
        type: 'bar',
        data: a.bjsr,
        itemStyle: { color: '#c0392b' },
      },
    ],
  }
}

export default {
  components: {
    VChart,
  },
  setup() {
    provide('THEME_KEY', 'light');
  },
  data() {
    return {
      options: {
        GCG: makeOption('GCG'),
        GPTFUZZER: makeOption('GPTFUZZER'),
        TAP: makeOption('TAP'),
      },
    }
  }
}
</script>

<template>
  <div>
    <el-divider />

    <el-row justify="center">
      <h1 class="section-title">Measurement Study</h1>
    </el-row>

    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="12">
        <p class="section-lead">
          Three representative LLM jailbreak families — gradient-based (GCG), evolutionary (GPTFUZZER), and
          multi-agent (TAP) — applied to LLM-based robots protected by the SafeRobot system prompt. In every case
          the orange bar (the attack bypassed refusal) towers over the red one (the robot actually did something
          harmful). That distance <b>is</b> the intent–behavior gap.
        </p>
      </el-col>
    </el-row>

    <!-- echarts 图表 -->
    <el-row justify="center">
      <el-col :xs="24" :sm="22" :md="20" :lg="18" :xl="16">
        <el-tabs class="chart-tabs" model-value="GCG">
          <el-tab-pane label="GCG" name="GCG">
            <v-chart class="chart" :option="options.GCG" autoresize />
          </el-tab-pane>
          <el-tab-pane label="GPTFUZZER" name="GPTFUZZER">
            <v-chart class="chart" :option="options.GPTFUZZER" autoresize />
          </el-tab-pane>
          <el-tab-pane label="TAP" name="TAP">
            <v-chart class="chart" :option="options.TAP" autoresize />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>

    <!-- saferobot 系统提示词的防御雷达图（论文 Figure 4） -->
    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="12">
        <el-image
          class="figure"
          src="./images/Figure_4.png"
          fit="contain"
          :preview-src-list="['./images/Figure_4.png']"
          hide-on-click-modal
        />
        <p class="caption">
          The SafeRobot system prompt helps unevenly across risk types: it suppresses direct damage (especially to
          people) far better than long-horizon damage such as chemical harm. It is also not universally deployable —
          it costs GPT-4o 82.67 points of task success rate, and barely secures Gemma-2-9B at all.
        </p>
      </el-col>
    </el-row>
  </div>

</template>

<style scoped>
/* 图表属性 */
.chart {
  height: 380px;
  margin-top: 10px;
}

.chart-tabs {
  margin-top: 20px;
}

/* 导语 */
.section-lead {
  font-size: 16px;
  line-height: 1.75rem;
  text-align: justify;
  margin: 20px 20px 0px 20px;
}

/* 论文插图 */
.figure {
  width: 100%;
  margin-top: 30px;
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
