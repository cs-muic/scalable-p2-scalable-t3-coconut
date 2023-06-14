<template>
  <v-container>
    <div class="row" align="center">
      <div class="col-sm-10">
        <h1>Videos</h1>
        <hr />
        <br /><br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Video</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(video, index) in vids" :key="index">
              <td>{{ video.vdo }}</td>
              <td>
                <div class="btn-group" role="group">
                  <v-btn
                    @click="
                      submit_video(video.vdo, video.vdo.split('.')[0] + '.gif')
                    "
                    depressed
                    color="primary"
                    >Convert video</v-btn
                  >
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <br /><br />
        <v-btn @click="submit_all" depressed color="primary"
          >Convert all videos</v-btn
        >
        <br /><br />
        <v-btn @click="getStatus" class="ma-2" outlined color="indigo"
          >Check Status</v-btn
        >
        <h2>Status: {{ status + " " + video_name }}</h2>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      vids: [],
      status: "",
      video_name: "",
    };
  },
  methods: {
    getVids() {
      const path = "http://0.0.0.0:5000/api/all_video";
      axios.get(path).then((res) => {
        this.vids = res.data.vids;
      });
    },
    async submit_all() {
      const bucket = { bucket: "video" };
      await axios
        .post("http://127.0.0.1:5000/api/enqueue_bucket", bucket)
        .catch((error) => {
          this.errorMessage = error.message;
          console.error("There was an error!", error);
        });
    },
    async submit_video(vdo, gif_name) {
      const data = { video: vdo, gif: gif_name };
      await axios
        .post("http://127.0.0.1:5000/api/enqueue", data)
        .catch((error) => {
          this.errorMessage = error.message;
          console.error("There was an error!", error);
        });
    },
    getStatus() {
      const path = "http://0.0.0.0:5000/api/get_status";
      axios.get(path).then((res) => {
        this.status = res.data.job_status;
        this.video_name = res.data.vid_name;
      });
    },
  },
  created() {
    this.getVids();
  },
  mounted() {
    this.getVids();
  },
};
</script>
