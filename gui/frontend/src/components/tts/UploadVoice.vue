<template>
  <label for="upload-voice">
    <el-button plain :icon="Upload" style="width: 32px" :loading="loading">
    </el-button>
    <input
      id="upload-voice"
      type="file"
      accept="audio/*"
      @change="handleUploadVoice"
      :disabled="loading"
    />
  </label>
  <el-select
    v-model="selectedVoice"
    placeholder="Chọn giọng nói"
    style="width: 200px"
  >
    <el-option
      v-for="(item, i) in listVoice"
      :key="i"
      :label="`Giọng ${i + 1}: ${item}`"
      :value="item"
    />
  </el-select>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { Upload } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { storeToRefs } from "pinia";
import { useAppStore } from "../../stores/app";

const appStore = useAppStore();
const { selectedVoice, listVoice, urlApi } = storeToRefs(appStore);
const loading = ref(false);

async function handleUploadVoice(event) {
  loading.value = true;
  const fileVoice = event.target.files[0];

  if (!fileVoice) {
    ElMessage({
      message: "Vui lòng chọn file âm thanh",
      type: "warning",
    });
    return;
  }
  const now = new Date();
  const voiceName = now.getTime();
  const formData = new FormData();
  formData.append("file", fileVoice);
  formData.append("audio_file_label", voiceName);

  try {
    const data = await axios.post(`${urlApi.value}/upload_audio/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (data.statusText == "OK") {
      ElMessage({
        message: "Tải giọng nói thành công",
        type: "success",
      });
    }

    appStore.getListVoice();
  } catch (error) {
    ElMessage({
      message: "Tải giọng nói lỗi",
      type: "error",
    });
  }

  loading.value = false;
}
</script>

<style scoped>
#upload-voice {
  position: absolute;
  left: 0;
  height: 32px;
  width: 32px;
  opacity: 0;
  cursor: pointer;
}
</style>
