import axios from "axios";
import { defineStore } from "pinia";
import { ListPlaybackDevice, GetUrlApi } from "../../wailsjs/go/main/App";

export const useAppStore = defineStore("app", {
  state: () => {
    return {
      listPlaybackDevice: [],
      playbackDeviceVB: undefined,
      listVoice: [],
      selectedVoice: undefined,
      alwaysTopStatus: false,
      urlApi: "",
    };
  },

  actions: {
    async init() {
      await this.getUrlApi();
      this.getListPlaybackDevice();
      this.getListVoice();
      
    },

    async getListPlaybackDevice() {
      this.listPlaybackDevice = await ListPlaybackDevice();
      this.listPlaybackDevice.forEach((e) => {
        if (e.Name === "CABLE Input (VB-Audio Virtual Cable)") {
          this.playbackDeviceVB = e.Key;
        }
      });
    },

    async getListVoice() {
      try {
        const data = await axios.get(`${this.urlApi}/list_voice/`);
        console.log(data);
        this.listVoice = data.data.message;
      } catch (error) {
        // console.log(error)
      }
    },

    async getUrlApi() {
      this.urlApi = await GetUrlApi();
    },
  },
});
