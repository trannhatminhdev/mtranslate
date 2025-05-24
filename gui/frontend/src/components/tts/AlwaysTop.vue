<template>
  <el-popover
    placement="top-start"
    trigger="hover"
    :content="
      alwaysTopStatus ? 'Bỏ hiển thị trên đầu' : 'Luôn luôn hiện thị trên đầu'
    "
  >
    <template #reference>
      <el-icon @click="toggleAlwaysTop()">
        <Unlock v-if="alwaysTopStatus" />
        <Lock v-else />
      </el-icon>
    </template>
  </el-popover>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useAppStore } from "../../stores/app";
import { Lock, Unlock } from "@element-plus/icons-vue";

const appStore = useAppStore();
const { alwaysTopStatus } = storeToRefs(appStore);

async function toggleAlwaysTop() {
  alwaysTopStatus.value = !alwaysTopStatus.value;
  window.runtime.WindowSetAlwaysOnTop(alwaysTopStatus.value);

  if (alwaysTopStatus.value) {
    await window.runtime.WindowSetMinSize(450, 150);
    await window.runtime.WindowSetSize(700, 150);
    await window.runtime.WindowCenter();
  } else {
    await window.runtime.WindowSetMinSize(450, 550);
    await window.runtime.WindowSetSize(700, 550);
    await window.runtime.WindowCenter();
  }
}
</script>
