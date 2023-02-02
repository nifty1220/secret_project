<template>
    <div id="header_area">
        <h1 id="stockx_title"> Stockx </h1>
        <button id="home_button" class="pixel_button" @click="goBack()">Home</button>
    </div>

    <div id="working_area">
        <div id="invoice_area">
<!--________________________________________________________________________________-->

            <div id="file_upload_area">
                <div class="main_header" id="upload_header"> Upload new sales </div>
                <label for="file_input">
                    <img id="upload_image" src="./../assets/upload.png">
                </label>
                <input type="file" id="file_input" accept=".csv, .xlsx" @change="setSelectedFile">
                <div id="selected_filename"> {{ selected_file }}</div>
                <button id="upload_sales_button" @click="goBack()">Upload</button>
            </div>

<!--________________________________________________________________________________-->

            <div id="seperator"></div>

<!--________________________________________________________________________________-->

            <div id="generate_area">
                <div class="main_header" id="generate_header"> Generate Invoices </div>

                <div id="date_area">
                    <div class="main_header" id="date_header"> Date Selection </div>
                    <br><br><br>
                    <select class="drowpdown" id="dropdown_month" v-model="selected_month">
                      <option disabled selected>Month</option>
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
                    <select class="drowpdown" id="dropdown_year" v-model="selected_year">
                      <option disabled selected>Year</option>
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

export default {
  name: 'StockxPage',
  emits: {
      backToPageSelection:null
  },
  props: {
      user_id: String,
      user_settings: Object,
      user_stockx_sales: Object,
  },
  created() {
  },
  data() {
      return {
          "selected_file": null,
          "selected_month": "Month",
          "selected_year": "Year",
      }
  },
  methods: {
      goBack() {
          this.$emit("backToPageSelection", true)
      },
      setSelectedFile(e) {
          this.selected_file = e.target.files[0].name
      }
  }
}
</script>


<style scoped>

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

.pixel_button:active {
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

#file_upload_area {
    //background-color: blue;
    height: 33%;
}

#upload_header {
    //background-color: orange;
    padding-top: 5%;
}

#upload_image {
    padding-top: 3.5%;
    margin-left: 20%;
    float:left;
    width: 12.5%;
    -webkit-filter: drop-shadow(5px 5px 0 black) drop-shadow(-1px -1px 0 black);
    filter: drop-shadow(4px 4px 0 black) drop-shadow(-1px -1px 0 black);
}

#upload_image:hover {
    cursor: pointer;
}

#upload_image:active {
    -webkit-filter: drop-shadow(11px 11px 0 black) drop-shadow(-1px -1px 0 black);
    filter: drop-shadow(1px 1px 0 black) drop-shadow(-1px -1px 0 black);
    padding-top: 4%;
    padding-left: 2px;
}

* {
    -moz-box-sizing: border-box;
    -webkit-box-sizing: border-box;
     box-sizing: border-box;
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
    margin-top: 7%;
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
    padding-top: 7.5%;
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
