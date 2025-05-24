<template>
  <Navigation v-if="!alwaysTopStatus" />
  <TTS v-if="!alwaysTopStatus" />
  <ConvertVoice v-if="alwaysTopStatus" />
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useAppStore } from "./stores/app";
import Navigation from "./components/layout/Navigation.vue";
import TTS from "./components/tts/TTS.vue";
import ConvertVoice from "./components/tts/ConvertVoice.vue";

const appStore = useAppStore();
const { alwaysTopStatus } = storeToRefs(appStore);
appStore.init();
</script>

<style>
.navigation {
  margin-bottom: 24px;
}
</style>
