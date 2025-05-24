<template>
  <el-select v-model="playbackDeviceVB" placeholder="Chọn thiết bị âm thanh" style="width: 260px">
    <el-option
      v-for="item in listPlaybackDevice"
      :key="item.Key"
      :label="item.Name"
      :value="item.Key"
    />
  </el-select>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useAppStore } from "../../stores/app";

const appStore = useAppStore();
const { playbackDeviceVB, listPlaybackDevice } = storeToRefs(appStore)
</script>