<template>
  <v-container>
    <div>
      <h1>GIF:</h1>
    </div>
    <v-row>
      <v-col
        v-for="(each, index) in all_gifs"
        :key="index"
        class="d-flex child-flex"
        cols="4"
      >
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      all_gifs: [],
      decodedStr: "",
    };
  },
  methods: {
    allGif() {
      const path = "http://0.0.0.0:5000/api/all_gif";
      console.log("aaaaa");
      axios.get(path).then((res) => {
        this.all_gifs = res.data.gifs;
      });
      console.log(this.all_gifs);
    },
  },
  created() {
    this.allGif();
  },
  mounted() {
    this.allGif();
  },
};
</script>
