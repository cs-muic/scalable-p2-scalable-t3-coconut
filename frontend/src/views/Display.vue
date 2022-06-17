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
        cols="6"
      >
        <v-col>
          <img v-bind:src="'data:image/jpeg;base64,' + each.gif_base64" />
          <v-btn @click="delete_gif(each.gif_name)" depressed color="primary">
            Delete gif</v-btn
          >
        </v-col>
      </v-col>
    </v-row>
    <br /><br /><br /><br />
    <v-btn @click="delete_all" depressed color="red">Delete all gifs</v-btn>
    <br /><br />
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      all_gifs: [],
      decodedStr: "",
      all_gif_name: [],
    };
  },
  methods: {
    allGif() {
      const path = "http://0.0.0.0:5000/api/all_gif";
      axios.get(path).then((res) => {
        this.all_gifs = res.data.gifs;
      });
    },
    async delete_all() {
      await axios
        .get("http://127.0.0.1:5000/api/delete_all_gif")
        .catch((error) => {
          this.errorMessage = error.message;
          console.error("There was an error!", error);
        });
      this.allGif();
    },
    async delete_gif(gif) {
      const data = { gif: gif };
      await axios
        .post("http://127.0.0.1:5000/api/delete_gif", data)
        .catch((error) => {
          this.errorMessage = error.message;
          console.error("There was an error!", error);
        });
      this.allGif();
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
