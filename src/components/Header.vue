<script lang="ts" setup>

import { ElIcon } from 'element-plus'
import { HomeFilled, SuccessFilled } from '@element-plus/icons-vue'

// 个人主页
const home = {
    name: "Xuancun Lu",
    link: "https://zjushine.github.io/",
}

// 项目主页
const logo = {
    name: "POEF",
    link: "#",
}

// 右侧更多菜单
const more_links = {
    "Paper": {
        name: "Paper (PDF)",
        link: "./POEF_NDSS2027.pdf",
    },
    "arXiv": {
        name: "arXiv - 2412.16633",
        link: "https://arxiv.org/abs/2412.16633",
    },
    "Code": {
        name: "Code - POEF",
        link: "https://github.com/ZJUshine/POEF",
    },
    "Dataset": {
        name: "Dataset - Harmful-Behavior",
        link: "https://github.com/ZJUshine/Harmful-Behavior",
    },
    "USSLab": {
        name: "USSLab, Zhejiang University",
        link: "http://usslab.org/",
    },
}

</script>

<template>
    <!-- 设置页首始终悬浮顶部 -->
    <el-affix :offset="0" :style="{width: '100%'}">

    <!-- 水平导航目录 -->
    <el-menu
        default-active="1"
        class="el-menu-demo"
        mode="horizontal"
        :ellipsis="false"
    >
        <!-- 个人主页 -->
        <el-menu-item index="0" >
            <el-icon :size="20"><HomeFilled /></el-icon>
            <a :href=home.link>{{ home.name }} </a>
        </el-menu-item>

        <!-- 项目主页 -->
        <el-menu-item index="1">
            <el-icon :size="20"><SuccessFilled /></el-icon>
            <a :href=logo.link>{{ logo.name }} </a>
        </el-menu-item>

        <!-- 更多栏目 -->
        <el-sub-menu index="2">
            <template #title>More</template>
            <el-menu-item index="2-1">
                <a :href=more_links.Paper.link>{{ more_links.Paper.name }}</a>
            </el-menu-item>
            <el-menu-item index="2-2">
                <a :href=more_links.arXiv.link>{{ more_links.arXiv.name }}</a>
            </el-menu-item>
            <el-menu-item index="2-3">
                <a :href=more_links.Code.link>{{ more_links.Code.name }}</a>
            </el-menu-item>
            <el-menu-item index="2-4">
                <a :href=more_links.Dataset.link>{{ more_links.Dataset.name }}</a>
            </el-menu-item>
            <el-menu-item index="2-5">
                <a :href=more_links.USSLab.link>{{ more_links.USSLab.name }}</a>
            </el-menu-item>
        </el-sub-menu>

    </el-menu>
    </el-affix>
</template>

<style>

/* 导航背景 */
.el-menu {
	background: none;
}

/* 下拉菜单宽度 */
.el-menu--popup {
	min-width: 100%;
}

/* 导航背景特效和阴影 */
.el-affix--fixed {
	box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
	background-image: radial-gradient(#ffffffca 1px,#ffffff 1px);
	background-size: 3px 3px;
}

/* 水平导航高度 */
.el-header {
    --el-header-height: 50px;
}

</style>

<style scoped>

/* 水平导航左右分区 */
.el-menu--horizontal > .el-menu-item:nth-child(2) {
    margin-right: auto;
}

/* 水平导航高度 */
.el-menu--horizontal {
    --el-menu-horizontal-height: 50px;
}

/* 取消鼠标焦点悬浮在链接上的颜色装饰 */
a:hover {
  color: inherit;
  border-bottom: none;
}

/* 链接装饰，取消下划线和链接颜色 */
a {
	text-decoration: None;
	color: inherit;
}

</style>
