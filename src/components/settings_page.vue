<template>
    <div id="header_area">
        <h1 id="settings_title"> Settings </h1>
        <button id="home_button" @click="goBack()">Home</button>
    </div>
    <div id="working_area">
        <img id="sevdesk_logo" src="./../assets/sevdesk.png">
        <div id="sevdesk_header" class="main_header"> SevDesk API Key </div><br><br><br><br><br><br>
        <input id="sevdesk_key" type="text" v-model="sevdesk_key"><br>

        <div id="seperator"></div>
        <div id="alias_header" class="main_header"> Alias Login </div>
        <input id="alias_email_input" type="text" v-model="alias_email" placeholder="E-Mail"><br>
        <input id="alias_password_input" type="text" v-model="alias_password" placeholder="Password"><br>

        <div id="seperator"></div>

        <div id="sort_options_header" class="main_header"> Sort Invoices by sale date </div>
        <br>
        <button id="sort_checkbox" @click="setSortOption"></button><br>

        <button id="save_settings_btn" @click="saveSettings()">Save Settings</button>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: 'SettingsPage',
  props: {
      user_id: String,
      user_settings: Array,
  },
  created() {
      this.sevdesk_key = this.user_settings["sevdesk_api_key"]
      this.alias_email = this.user_settings["alias_email"]
      this.alias_password = this.user_settings["alias_password"]
      console.log("Settings Module received this data:")
      console.log(this.user_settings)
  },
  data() {
      return {
          sevdesk_key: "",
          sort_by_sale_date: false,
          alias_email: "",
          alias_password: ""
      }
  },
  methods: {
      goBack() {
          this.$emit("backToPageSelection", true)
      },
      saveSettings() {
          console.log(this.sevdesk_key)
          axios({
                  method: "POST",
                  url: 'http://10.0.0.9:5000/save_user_settings',
                  data: {},
                  headers: {
                      "user_id": this.user_id,
                      "sevdesk_api_key": this.sevdesk_key,
                      "alias_email": this.alias_email,
                      "alias_password": this.alias_password,
                      "sort_option": this.sort_by_sale_date,
                  },
              })
              .then((response) => {
                  let reponse_data = response.data
                  console.log(reponse_data)
                  this.$emit("retrieveUserData", this.user_id)
                  //toast("Error trying to save!", {autoClose: 1000,});
                  toast("Settings saved successfully!", {
                      autoClose: 2000,
                      progressClassName: 'Toastify__progress-bar-theme--dar',
                      toastStyle: {
                          fontSize: '15px',
                          color:"black",
                          "font-family": "Square",
                          src: "url('./../../fonts/Square.TTF')",
                          'margin-left': '27.5%',
                          'letter-spacing': '2px',
                          'text-decoration': 'none',
                          'text-transform': 'uppercase',
                          cursor: 'pointer',
                          border: '3px solid',
                          padding: '0.25em 0.5em',
                          'box-shadow': '0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px',
                          position: 'relative',
                          'user-select': 'none',
                          '-webkit-user-select': 'none',
                          'touch-action': 'manipulation',
                          "toastify-color-progress-dark": "#bb86fc",
                      },
                  });
              });
      },
      setSortOption(){
          this.sort_by_sale_date = !this.sort_by_sale_date
      },
  }
}
</script>


<style scoped>

#header_area {
    margin-top: 0;
    align-items: center;
    display: flex;
}

#settings_title {
    width: 25%;
    margin-left: 37.5%;
    font-family: SuperMario;
    src: url('./../../fonts/pixel.TTF');
    color: white;
    font-size: 400%;
}

h1 {
    text-shadow: black 7.5px 7.5px;
    margin: 0;
}

#home_button {
    width: 7.5%;
    margin-left: 27.5%;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    position: relative;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#working_area {
    background-color: rgba(255, 255, 255, .075);
    margin-left: 2.5%;
    margin-right: 2.5%;
    margin-top: 1%;
    height: 97.5%;
    border-radius: 25px;
    box-shadow: rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px;
}

.main_header {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 200%;
    color: white;
    text-shadow: black 2.5px 2.5px;
}

#sevdesk_logo {
    float:left;
    margin-left: 38.5%;
    margin-top: 2.5%;
    height: 50px;
    width: 80px;
    object-fit: cover;
    object-position: -20% 0;
}

#sevdesk_header {
    float:left;
    margin-top: 3%;
    margin-left: 1%;
}

#sevdesk_key {
    margin-top: 1%;
    width: 15%;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#alias_header {
    margin-top: 3%;
    margin-left: 1%;
}

#alias_email_input {
    margin-top: 1%;
    width: 15%;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#alias_password_input {
    margin-top: 1%;
    width: 15%;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#sort_options_header {
    margin-top: 3%;
}

#sort_checkbox {
    height: 25px;
    width: 25px;
    color:white;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    position: relative;
}

#save_settings_btn {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 125%;
    letter-spacing: 2px;
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    cursor: pointer;
    border: 3px solid;
    padding: 0.25em 0.5em;
    box-shadow: 0px 0px 0px 0px, 1px 1px 0px 0px, 2px 2px 0px 0px, 3px 3px 0px 0px, 4px 4px 0px 0px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    margin-top: 2.5%;
    position: relative;
}

#save_settings_btn:active, #sort_checkbox:active, #home_button:active {
    box-shadow: 0px 0px 0px 0px;
    top: 2px;
    left: 2px;
}

#seperator{
    margin: 0 auto;
    margin-top: 3%;
    height: 1px;
    width: 50%;
    border-radius: 100px;
    -webkit-filter: blur(2.5px);
    -moz-filter: blur(2.5px);
    -o-filter: blur(2.5px);
    -ms-filter: blur(2.5px);
    filter: blur(2.5px);
    background-color: rgba(255, 255, 255, 1.5);
}
</style>
