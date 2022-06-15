<template>
  <v-container>
    <div class="control-center">
      <h1>Enter video you want to convert to gif</h1>
    </div>
    <div id="app">
      <v-app id="inspire">
        <v-form>
          <v-container>
            <v-row justify="space-around">
              <v-col cols="12" sm="6" md="3">
                <v-text-field label="Video" outlined></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-row justify="space-around">
          <v-btn depressed color="primary">Convert video</v-btn>
          <v-btn depressed color="primary">Convert all videos</v-btn>
        </v-row>
      </v-app>
    </div>
  </v-container>
</template>
