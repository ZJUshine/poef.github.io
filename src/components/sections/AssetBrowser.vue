<script setup>
import { ref, computed, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import manifest from '@/assets/asset-manifest.json'

// Base URL for OSS-hosted assets, injected at build time via VITE_OSS_BASE_URL.
// e.g. https://your-bucket.oss-cn-hangzhou.aliyuncs.com
const ossBase = import.meta.env.VITE_OSS_BASE_URL?.replace(/\/$/, '') ?? ''

const videoSet = new Set(manifest.videos)

const allItems = manifest.gltfs
  .map(stem => ({
    stem,
    label: stem.replace(/_/g, ' '),
    gltfUrl: `${ossBase}/gltfs/${stem}.gltf`,
    videoUrl: videoSet.has(stem) ? `${ossBase}/videos/${stem}.mp4` : null,
  }))
  .sort((a, b) => a.label.localeCompare(b.label))

const search = ref('')
const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return allItems
  return allItems.filter(item => item.label.includes(q))
})

const selected = ref(allItems[0] ?? null)
const viewMode = ref(allItems[0]?.videoUrl ? 'video' : 'model')

function select(item) {
  selected.value = item
  viewMode.value = item.videoUrl ? 'video' : 'model'
}

watch(filtered, (list) => {
  if (selected.value && !list.find(i => i.stem === selected.value.stem)) {
    const next = list[0] ?? null
    if (next) select(next)
    else selected.value = null
  }
})
</script>

<template>
  <div>
    <el-divider />

    <el-row justify="center">
      <h1 class="section-title">Harmful-Behavior Preview</h1>
    </el-row>

    <el-row justify="center">
      <el-col :xs="24" :sm="22" :md="20" :lg="18" :xl="16">
        <div class="browser">

          <!-- Left: searchable list -->
          <aside class="list-panel">
            <el-input
              v-model="search"
              :prefix-icon="Search"
              placeholder="Search actions…"
              clearable
              class="search-input"
            />
            <ul class="item-list" role="listbox" aria-label="Action list">
              <li
                v-for="item in filtered"
                :key="item.stem"
                class="item-row"
                :class="{ active: selected?.stem === item.stem }"
                role="option"
                :aria-selected="selected?.stem === item.stem"
                tabindex="0"
                @click="select(item)"
                @keydown.enter.space.prevent="select(item)"
              >
                <span class="item-label">{{ item.label }}</span>
                <span class="item-badges">
                  <el-tag v-if="item.videoUrl" size="small" type="success" effect="plain">video</el-tag>
                  <el-tag size="small" type="info" effect="plain">3D</el-tag>
                </span>
              </li>
              <li v-if="filtered.length === 0" class="empty-row">No results</li>
            </ul>
          </aside>

          <!-- Right: viewer -->
          <section class="viewer-panel" aria-live="polite">
            <template v-if="selected">
              <div class="viewer-header">
                <h3 class="viewer-title">{{ selected.label }}</h3>
                <el-radio-group
                  v-if="selected.videoUrl"
                  v-model="viewMode"
                  size="small"
                  class="view-toggle"
                >
                  <el-radio-button value="video">Video</el-radio-button>
                  <el-radio-button value="model">3D Model</el-radio-button>
                </el-radio-group>
              </div>

              <!-- Video player -->
              <div v-if="viewMode === 'video' && selected.videoUrl" class="media-wrap">
                <video
                  :key="selected.videoUrl"
                  :src="selected.videoUrl"
                  controls
                  playsinline
                  class="media-video"
                  :aria-label="`Video: ${selected.label}`"
                />
              </div>

              <!-- 3D model viewer -->
              <div v-else class="media-wrap">
                <model-viewer
                  :key="selected.gltfUrl"
                  :src="selected.gltfUrl"
                  camera-controls
                  auto-rotate
                  shadow-intensity="1"
                  class="media-model"
                  :alt="`3D model: ${selected.label}`"
                />
              </div>
            </template>

            <div v-else class="empty-viewer">
              <p>Select an action to preview it.</p>
            </div>
          </section>

        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.browser {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 16px;
  margin-top: 24px;
  min-height: 520px;
}

@media (max-width: 768px) {
  .browser { grid-template-columns: 1fr; }
}

/* ── List panel ── */
.list-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid var(--el-border-color);
  border-radius: 8px;
  padding: 12px;
  background: var(--el-bg-color);
}

.search-input { flex-shrink: 0; }

.item-list {
  list-style: none;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  flex: 1;
  max-height: 460px;
}

.item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 150ms ease;
  outline-offset: 2px;
}

.item-row:hover { background: var(--el-fill-color-light); }

.item-row.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 500;
}

.item-row:focus-visible { outline: 2px solid var(--el-color-primary); }

.item-label {
  font-size: 13px;
  line-height: 1.4;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-badges {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.empty-row {
  padding: 16px 10px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
  text-align: center;
}

/* ── Viewer panel ── */
.viewer-panel {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--el-border-color);
  border-radius: 8px;
  padding: 16px;
  background: var(--el-bg-color);
}

.viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.viewer-title {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.media-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  overflow: hidden;
  background: var(--el-fill-color-lighter);
  min-height: 360px;
}

.media-video {
  width: 100%;
  max-height: 440px;
  display: block;
  border-radius: 4px;
}

.media-model {
  width: 100%;
  height: 440px;
  border-radius: 4px;
}

.empty-viewer {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-secondary);
}
</style>
