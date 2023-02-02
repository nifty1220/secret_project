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

        <div id="alias_container">
            <div id="alias_header" class="main_header"> Alias Login </div>
            <input id="alias_email_input" type="text" v-model="alias_email" placeholder="E-Mail"><br>
            <input id="alias_password_input" type="text" v-model="alias_password" placeholder="Password"><br>
        </div>
        <div id="stockx_container">
            <img id="cookie_image" src="./../assets/cookie.png">
            <div id="stockx_header" class="main_header"> StockX Cookie </div>
            <textarea  id="stockx_cookie_input" type="textarea" v-model="stockx_cookies" placeholder="Paste Cookies here..."></textarea>
        </div>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <div id="seperator"></div>

        <div id="sort_options_header" class="main_header"> Sort Invoices by sale date </div>
        <br>
        <button id="sort_checkbox" @click="setSortOption">{{checkbox_text}}</button><br>

        <button id="save_settings_btn" @click="saveSettings()">Save Settings</button>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: 'SettingsPage',
  emits: {
      backToPageSelection:null,
      retrieveUserData:null,
  },
  props: {
      user_id: String,
      user_settings: Object
  },
  created() {
      this.sevdesk_key = this.user_settings["sevdesk_api_key"]
      this.alias_email = this.user_settings["alias_email"]
      this.alias_password = this.user_settings["alias_password"]
      this.stockx_cookies = JSON.stringify(this.user_settings["stockx_cookie"])
      this.sort_by_sale_date = this.user_settings["sort_invoice_by_sale_date"]
  },
  data() {
      return {
          sevdesk_key: "",
          sort_by_sale_date: false,
          checkbox_text: "",
          alias_email: "",
          alias_password: "",
          stockx_cookies: "TEST",
      }
  },
  watch: {
      sort_by_sale_date() {
          if (this.sort_by_sale_date == true) {
              this.checkbox_text="✓"
          } else {
              this.checkbox_text=""
          }
      }
  },
  methods: {
      goBack() {
          this.$emit("backToPageSelection", true)
      },
      saveSettings() {
          console.log(this.sort_by_sale_date)
          axios({
                  method: "POST",
                  url: 'http://10.0.0.9:5000/save_user_settings',
                  data: {
                      "sevdesk_api_key": this.sevdesk_key,
                      "alias_email": this.alias_email,
                      "alias_password": this.alias_password,
                      "sort_option": this.sort_by_sale_date,
                      "stockx_cookies": this.stockx_cookies
                  },
                  headers: {
                      "Content-Type": "application/json",
                      "user_id": this.user_id
                  },
              })
              .then((response) => {
                  let reponse_data = response.data
                  console.log(reponse_data)
                  this.$emit("retrieveUserData", this.user_id)

                  toast("Settings saved successfully!", {
                      autoClose: 2000,
                      progressClassName: 'Toastify__progress-bar-theme--dark',
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
    margin-left: 39%;
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

#alias_container {
    float:left;
    width: 25%;
    height: 15em;
    margin-left: 22.5%;
    margin-top: 1.5%;
}

#stockx_container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    float:left;
    width: 25%;
    height: 15em;
    margin-left: 5%;
    margin-top: 1.5%;
}

#alias_header {
    margin-top: 3%;
    margin-left: 1%;
}

#alias_email_input {
    margin-top: 3%;
    width: 75%;
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
    margin-top: 3%;
    width: 75%;
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

#cookie_image {
    height: 50px;
    width: 50px;
    margin-left: 15%;
    -webkit-filter: drop-shadow(5px 5px 0 black) drop-shadow(-1px -1px 0 black);
    filter: drop-shadow(2px 2px 0 black) drop-shadow(-1px -1px 0 black);
}

#stockx_header {
    margin-top: 7.5px;
    width: 240px;
    height: 40px;
    float: left;
}

#stockx_cookie_input {
    resize: none;
    margin-top: 1%;
    height: 65%;
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
    flex:100%;
    order: 3;
}

#sort_options_header {
    margin-top: 1.5%;
}

#sort_checkbox {
    height: 25px;
    width: 25px;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    text-decoration: none;
    text-transform: uppercase;
    color: #000;
    font-weight: bold;
    cursor: pointer;
    border: 3px solid;
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
    margin-top: 3%;
    position: relative;
}

#save_settings_btn:active, #sort_checkbox:active, #home_button:active {
    box-shadow: 0px 0px 0px 0px;
    top: 2px;
    left: 2px;
}

#seperator{
    margin: 0 auto;
    margin-top: 2%;
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
