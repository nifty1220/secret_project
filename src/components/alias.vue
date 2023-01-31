<template>

    <div id="header_area">
        <h1 id="stockx_title"> Alias </h1>
        <button id="home_button" class="pixel_button" @click="goBack()">Home</button>
    </div>

    <div id="working_area">
        <div id="invoice_area">
<!--________________________________________________________________________________-->

            <div id="refresh_area">
                <div class="main_header" id="upload_header"> Refresh sales </div>

                <div v-if="refresh_active" class="atom-spinner">
                  <div class="spinner-inner">
                    <div class="spinner-line"></div>
                    <div class="spinner-line"></div>
                    <div class="spinner-line"></div>
                    <div class="spinner-circle">
                      &#9679;
                    </div>
                  </div>
                </div>
                <br><br>
                <div v-if="!refresh_active" id="refresh_msg" class="main_header">{{ refresh_message }}</div>
                <br><br><br>
                <button id="upload_sales_button" @click="refreshAliasSales()">Refresh</button>
            </div>

<!--________________________________________________________________________________-->

            <div id="seperator"></div>

<!--________________________________________________________________________________-->

            <div id="generate_area">
                <div class="main_header" id="generate_header"> Generate Invoices </div>
                <div id="date_area">
                    <div class="main_header" id="date_header"> Date Selection </div>
                    <br><br><br>
                    <select class="drowpdown" id="dropdown_month">
                      <option value="1">January</option>
                      <option value="2">Febuary</option>
                      <option value="3">March</option>
                      <option value="4">April</option>
                      <option value="5">May</option>
                      <option value="6">June</option>
                      <option value="7">July</option>
                      <option value="8">August</option>
                      <option value="9">September</option>
                      <option value="10">October</option>
                      <option value="11">November</option>
                      <option value="12">December</option>
                    </select>
                    <select class="drowpdown" id="dropdown_year">
                      <option value="2020">2020</option>
                      <option value="2021">2021</option>
                      <option value="2022">2022</option>
                      <option value="2023">2023</option>
                    </select>
                </div>
                <div id="actions_area">
                    <div class="main_header" id="actions_header"> Actions </div>
                    <br><br><br>
                    <button id="btn_generate" class="pixel_button" @click="goBack()">Generate</button>
                    <!--<button id="btn_download" class="pixel_button" @click="goBack()" disabled >Download</button>-->
                    <button id="btn_gendown" class="pixel_button" @click="goBack()">Generate + Download</button>
                </div>
            </div>
        </div>
        <div id="label_area">
            <div class="main_header" id="label_header"> Label Generator </div>
            <div class="main_header" id="label_header"> COMING SOON </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: 'AliasPage',
  props: {
      user_id: String,
      user_settings: Array,
      user_alias_sales: Array,
  },
  created() {
      this.alias_email = this.user_settings["alias_email"]
      this.alias_password = this.user_settings["alias_password"]
      console.log("Alias Module received this data:")
      this.user_alias_sales.forEach(element => console.log(element));
  },
  data() {
      return {
          refresh_active: false,
          refresh_message: "",
          alias_email: "",
          alias_password: ""
      }
  },
  methods: {
      goBack() {
          this.$emit("backToPageSelection", true)
      },
      refreshAliasSales() {

          this.refresh_active = true

          axios({
                  method: "POST",
                  url: 'http://10.0.0.9:5000/refresh_alias_sales',
                  data: {
                      "alias_email": this.alias_email,
                      "alias_password": this.alias_password,
                  },
                  headers: {
                      "Content-Type": "application/json",
                      "user_id": this.user_id,

                  },
              })
              .then((response) => {
                  let result_msg = ""

                  if (response.data.data == 200) {
                      result_msg = "Successfully updated Alias sales!"
                  } else if (response.data.data == 401) {
                      result_msg = "Error logging into alias account! Please check your credentials"
                  } else {
                      result_msg = "Unknown error"
                  }

                  toast(result_msg, {
                      autoClose: 2000,
                      progressClassName: 'Toastify__progress-bar-theme--dark',
                      toastStyle: {
                          fontSize: '15px',
                          color:"black",
                          "font-family": "Square",
                          src: "url('./../../fonts/Square.TTF')",
                          'letter-spacing': '2px',
                          'text-decoration': 'none',
                          'text-transform': 'uppercase',
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
                  this.refresh_active = false

              });
      },
  }
}
</script>


<style scoped>

.atom-spinner, .atom-spinner * {
      box-sizing: border-box;
    }

    .atom-spinner {
      float:left;
      margin-left: 47%;
      margin-top: 2%;
      height: 60px;
      width: 60px;
      overflow: hidden;
    }

    .atom-spinner .spinner-inner {
      position: relative;
      display: block;
      height: 100%;
      width: 100%;
    }

    .atom-spinner .spinner-circle {
      display: block;
      position: absolute;
      color: #ff1d5e;
      font-size: calc(60px * 0.24);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }

    .atom-spinner .spinner-line {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      animation-duration: 1s;
      border-left-width: calc(60px / 25);
      border-top-width: calc(60px / 25);
      border-left-color: #ff1d5e;
      border-left-style: solid;
      border-top-style: solid;
      border-top-color: transparent;
    }

    .atom-spinner .spinner-line:nth-child(1) {
      animation: atom-spinner-animation-1 1s linear infinite;
      transform: rotateZ(120deg) rotateX(66deg) rotateZ(0deg);
    }

    .atom-spinner .spinner-line:nth-child(2) {
      animation: atom-spinner-animation-2 1s linear infinite;
      transform: rotateZ(240deg) rotateX(66deg) rotateZ(0deg);
    }

    .atom-spinner .spinner-line:nth-child(3) {
      animation: atom-spinner-animation-3 1s linear infinite;
      transform: rotateZ(360deg) rotateX(66deg) rotateZ(0deg);
    }

    @keyframes atom-spinner-animation-1 {
      100% {
        transform: rotateZ(120deg) rotateX(66deg) rotateZ(360deg);
      }
    }

    @keyframes atom-spinner-animation-2 {
      100% {
        transform: rotateZ(240deg) rotateX(66deg) rotateZ(360deg);
      }
    }

    @keyframes atom-spinner-animation-3 {
      100% {
        transform: rotateZ(360deg) rotateX(66deg) rotateZ(360deg);
      }
    }
#header_area {
    margin-top: 0;
    align-items: center;
    display: flex;
}

#stockx_title {
    width: 25%;
    margin-left: 37.5%;
    font-family: SuperMario;
    src: url('./../../fonts/pixel.TTF');
    color: white;
    font-size: 400%;
}

#refresh_msg {
    float:left;
    margin-left: 35%;
    font-size: 125%;
    color:green;
}

h1 {
    text-shadow: black 7.5px 7.5px;
    margin: 0;
}

.pixel_button {
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

#pixel_button:active {
    box-shadow: 0px 0px 0px 0px;
    top: 2px;
    left: 2px;
}

#home_button {
    margin-left: 27.5%;
    width: 7.5%;
}

#working_area {
    margin-top: 1%;
    background-color: rgba(255, 255, 255, .075);
    margin-left: 2.5%;
    margin-right: 2.5%;
    height: 97.5%;
    border-radius: 25px;
    box-shadow: rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px;
}

#invoice_area {
    //background-color: red;
    float:left;
    width: 50%;
    height: 100%;
}

#refresh_area {
    //background-color: blue;
    height: 33%;
}

#upload_header {
    //background-color: orange;
    padding-top: 5%;
}

#upload_image {
    padding-top: 2.5%;
    margin-left: 20%;
    float:left;
    width: 12.5%;
}

#upload_image:hover {
    cursor: pointer;
}

#selected_filename {
    width: 35%;
    float:left;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 150%;
    color: white;
    text-shadow: black 2.5px 2.5px;
    margin-top: 7.5%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

#file_input {
    display: none;
}

#upload_sales_button {
    margin-top: 1%;
    margin-left: 42.5%;
    float:left;
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
    position: relative;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#upload_sales_button:active {
    box-shadow: 0px 0px 0px 0px;
    top: 2px;
    left: 2px;
}

#seperator{
    margin: 0 auto;
    margin-top: 3%;
    height: 1px;
    width: 75%;
    border-radius: 100px;
    -webkit-filter: blur(2.5px);
    -moz-filter: blur(2.5px);
    -o-filter: blur(2.5px);
    -ms-filter: blur(2.5px);
    filter: blur(2.5px);
    background-color: rgba(255, 255, 255, 1.5);
}

#generate_area {
    height: 66.6%;
    //background-color: red;
}

#generate_header {
    padding-top: 5%;
}

.drowpdown {
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

#date_area {
    //background-color: blue;
    margin-top: 5%;
}

#date_header {
    float:left;
    margin-left: 20%;
    font-size: 150%;
}

#dropdown_month {
    float:left;
    margin-left: 20%;
}

#dropdown_year {
    float:left;
    margin-left: 2%;
}

#actions_area {
    //background-color: green;
    margin-top: 10%;
}

#actions_header{
    float:left;
    margin-left: 20%;
    font-size: 150%;
}

#button_area {
}

#btn_download {
}

#btn_generate {
    float:left;
    margin-left: 20%;
}

#btn_gendown {
    float:left;
    margin-left: 2%;
}

#label_area {
    width: 50%;
    float:left;
}

#label_header {
    padding-top: 5%;
    margin-left: 0%;
}

.main_header {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 200%;
    color: white;
    text-shadow: black 2.5px 2.5px;
}


</style>
