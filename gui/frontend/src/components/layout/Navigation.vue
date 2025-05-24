<template>
  <el-container>
    <el-button type="primary" plain :icon="HomeFilled">TTS</el-button>
    <el-button type="info" link :icon="Link" @click="openGithub">
      Github
    </el-button>
  </el-container>
</template>

<script setup>
import { HomeFilled, Link } from "@element-plus/icons-vue";

function openGithub() {
  window.runtime.BrowserOpenURL(
    "https://github.com/trannhatminhdev/mtranslate"
  );
}
</script>
