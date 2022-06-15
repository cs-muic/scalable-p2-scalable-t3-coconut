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
                  <v-btn depressed color="primary">Convert video</v-btn>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <br /><br />
        <v-btn depressed color="primary">Convert all videos</v-btn>
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
    };
  },
  methods: {
    getVids() {
      const path = "http://0.0.0.0:5000/api/all_video";
      axios.get(path).then((res) => {
        this.vids = res.data.vids;
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
