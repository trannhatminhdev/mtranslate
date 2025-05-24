<template>
  <div
    :class="{
      'convert-voice-alaways-top': alwaysTopStatus,
    }"
  >
    <el-input
      v-model="textVoice"
      :rows="alwaysTopStatus ? 2 : 5"
      type="textarea"
      placeholder="Nhấn Enter để chuyển đổi giọng nói"
      resize="none"
      show-word-limit
      :maxlength="100"
      @keydown.enter.exact.prevent="convertVoiceTrigger"
    />

    <el-row
      :class="alwaysTopStatus ? 'mt-2' : 'mt-3'"
      justify="space-between"
      align="middle"
    >
      <el-button
        plain
        :icon="Promotion"
        @click="convertVoiceTrigger"
        :loading="loading"
      >
        Chuyển đổi
      </el-button>
      <AlwaysTop v-if="alwaysTopStatus" />
    </el-row>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useAppStore } from "../../stores/app";
import { Promotion } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import "element-plus/es/components/message/style/css";
import { StartPlaybackDevice } from "../../../wailsjs/go/main/App";
import AlwaysTop from "./AlwaysTop.vue";

const appStore = useAppStore();
const { alwaysTopStatus, playbackDeviceVB, selectedVoice } = storeToRefs(appStore);
const textVoice = ref("");
const loading = ref(false);

function convertVoiceTrigger() {
  if (loading.value) return;

  if (isNaN(playbackDeviceVB.value)) {
    ElMessage({
      message: "Vui lòng chọn thiết bị âm thanh",
      type: "warning",
    });
    return;
  }

  if (!selectedVoice.value) {
    ElMessage({
      message: "Vui lòng chọn giọng nói",
      type: "warning",
    });
    return;
  }

  convertVoiceHandle(playbackDeviceVB.value);
}

async function convertVoiceHandle(keyDevice) {
  if (!textVoice.value) {
    ElMessage({
      message: "Vui lòng nhập văn bản",
      type: "warning",
    });
    return;
  }
  loading.value = true;

  try {
    await StartPlaybackDevice(keyDevice, textVoice.value);
  } catch (error) {
    ElMessage({
      message: "Không thể tạo giọng nói",
      type: "error",
    });
  } finally {
    textVoice.value = "";
    loading.value = false;
  }
}
</script>

<style scoped>
.convert-voice-alaways-top {
  position: fixed;
  top: 10px;
  left: 10px;
  right: 10px;
}
</style>
