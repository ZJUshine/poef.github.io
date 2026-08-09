<script>
import { Swiper, SwiperSlide} from 'swiper/vue';
import { Navigation, Pagination, Autoplay} from 'swiper/modules';
import 'swiper/css/bundle';

export default {
  components: {
      Swiper,
      SwiperSlide,
      Navigation,
      Pagination,
      Autoplay,
    },
  data() {
    return {
      modules: [
        Navigation,
        Pagination,
        Autoplay,
      ],
      // 轮播真实世界实验的照片（来自论文 Figure 6/7/8）
      images: [
        {
          path: "./images/Figure_6.png",
          caption: "Real-world setups. Left: the Franka Emika Panda arm with a fixed RGB-D camera and a microphone. Right: the Unitree G1 humanoid using its head camera and chest microphone array. Both are paired with a speaker that injects the adversarial voice instruction.",
        },
        {
          path: "./images/Figure_7_compress.png",
          caption: "Ten real-world jailbreak scenarios. Top: the full policy sequence for “pour water on socket” on both platforms. Bottom: snapshots of the remaining scenarios covering human, object, and environment risks.",
        },
        {
          path: "./images/Figure_8.png",
          caption: "Behavior jailbreak on the commercial Unitree G1 humanoid system, showing that POEF transfers from manipulation to whole-body motion control.",
        },
        {
          path: "./images/Figure_1_2.png",
          caption: "Conceptually, POEF achieves policy generation and physical effectiveness at the same time — the quadrant that prior jailbreaks never reach.",
        },
      ],
    }
  }
}
</script>

<template>
  <div>
    <el-divider />

    <el-row justify="center">
      <h1 class="section-title">Real-World Attack Pipeline</h1>
    </el-row>

    <el-row justify="center">
      <el-col :span="24">
        <!-- 设置轮播图：循环播放、响应式、导航和分页、自动播放 -->
        <!-- autoHeight 让容器贴合当前这张图的高度，否则矮图下方会留一大片空白 -->
        <swiper
          :loop="true"
          :autoHeight="true"
          :slidesPerView="1"
          :modules="modules"
          :navigation="{
            hideOnClick:true,
          }"
          :pagination="{
            hideOnClick:true,
            clickable:true,
            type:'bullets'
          }"
          :autoplay="{
            delay:6000,
            disableOnInteraction:false,
            pauseOnMouseEnter:true,
          }"
          >
          <swiper-slide v-for="image in images" :key="image.path">
            <div class="slide">
              <el-image
                :src="image.path"
                fit="contain"
                :preview-src-list="[image.path]"
                hide-on-click-modal
              />
              <p class="caption">{{ image.caption }}</p>
            </div>
          </swiper-slide>
        </swiper>
      </el-col>
    </el-row>
  </div>
</template>

<style>

/* 设置Swiper风格 */
.swiper {
  --swiper-theme-color: #c0392b;
}

/* 给分页圆点留出位置，避免压住图注 */
.swiper-pagination {
  position: static !important;
  margin-top: 8px;
}

</style>

<style scoped>

/* 每一张幻灯片，限制最大宽度让单张图不至于横跨整个屏幕 */
.slide {
  padding: 20px 16px 0px 16px;
  max-width: 1100px;
  margin: 0 auto;
}

.slide .el-image {
  width: 100%;
  cursor: zoom-in;
}

/* 图注 */
.caption {
  font-size: 14px;
  line-height: 1.6rem;
  color: var(--el-text-color-secondary);
  text-align: justify;
  margin: 10px 0px 0px 0px;
}

</style>
