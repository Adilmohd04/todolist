const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    projectId: "4hucyo",
    video: true,
    baseUrl: 'http://127.0.0.1:8000',
    "videoCompression": 32, 
  "videoUploadOnPasses": false,
  "videosFolder": "cypress/videos",
    requestTimeout: 60000, 
    defaultCommandTimeout: 60000, 
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
