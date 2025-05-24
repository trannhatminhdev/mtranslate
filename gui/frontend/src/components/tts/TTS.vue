<template>
  <h1 class="mt-5 pt-2 text-xl font-semibold">
    Công cụ chuyển văn bản thành giọng nói
  </h1>
  <p class="text-sm pb-4">Phiên bản: 1.0</p>

  <el-row
    class="mt-5 mb-5"
    justify="space-between"
    align="middle"
    style="gap: 12px"
  >
    <el-row style="gap: 12px">
      <UploadVoice />
      <PlaybackDevice />
    </el-row>

    <AlwaysTop />
  </el-row>

  <ConvertVoice />
</template>
<script setup>
import { storeToRefs } from "pinia";
import { useAppStore } from "../../stores/app";
import PlaybackDevice from "./PlaybackDevice.vue";
import UploadVoice from "./UploadVoice.vue";
import AlwaysTop from "./AlwaysTop.vue";
import ConvertVoice from "./ConvertVoice.vue";

const appStore = useAppStore();
const { playbackDeviceVB } = storeToRefs(appStore);
</script>
