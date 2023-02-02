<template>
<div id="container_login_page">
    <div id="container_header">
        <h1 id="login_title"> AT Mafia Invoice Manager </h1>
    </div>
    <div id="container_login_form">
        <p id="login_license_text"> Enter License Key </p>
        <input @click="clear_license_error" id="login_license_input" type="text" v-model="license_key">
        <br>
        <button id="login_button" @click="loginUser()">Login</button>
        <p v-if="license_error" id="license_key_error"> {{ license_error_msg }} </p>
    </div>
</div>
</template>

<script>

import axios from 'axios'

export default {
    name: 'LoginPage',
    data() {
        return {
            license_key: "",
            license_error: false,
            license_error_msg: ""
        }
    },
    methods: {
        loginUser() {

            if(this.license_key.length == 20) {

            axios({
                    method: "GET",
                    url: 'http://127.0.0.1:5000/login_user',
                    data: {},
                    headers: {
                        "Content-Type": "application/json",
                        "key": this.license_key
                    },
                })
                .then((response) => {
                    let user_id = response.data.data
                    if(user_id == 0 ) {
                        this.license_error = true
                        this.license_error_msg = "License key not found!"
                    } else {
                        this.$emit("retrieveUserData", user_id[0][0])
                        this.$emit("continueSiteSelectionPage", true)
                    }
                });
            } else {
                this.license_error = true
                this.license_error_msg = "Invalid License entered!"
            }
        },
        clear_license_error() {
            this.license_error = false
        }
    }
}
</script>

<style scoped>
#container_header {
    margin-top: 7.5%;
}

#login_title {
    font-family: SuperMario;
    src: url('./../../fonts/pixel.TTF');
    color: white;
    font-size: 400%;

    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

h1 {
    text-shadow: black 7.5px 7.5px;
}

#container_login_form {
    margin-top: 7.5%;
}

#license_key_error {
    color:red;
    font-size: 125%;
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    text-shadow: black 2.5px 2.5px;
}

#login_license_text {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 200%;
    color: white;
    text-shadow: black 2.5px 2.5px;
}

#login_license_input {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    text-align: center;
    border: 3px solid #000;
    border-radius: 5px;
    height: 50px;
    line-height: normal;
    color: #282828;
    width: 25%;
    box-sizing: border-box;
    font-size: 16px;
    padding: 0 6px;
    padding-left: 12px;
}

#login_button {
    margin-top: 2%;
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

#login_button:active {
    box-shadow: 0px 0px 0px 0px;
    top: 2px;
    left: 2px;
}

@media (min-width: 768px) {
    #login_button {
        padding: 0.2% 3.5%;
    }
}

@font-face {
    font-family: "Square";
    src: url('./../../fonts/Square.TTF');
}

@font-face {
    font-family: "SuperMario";
    src: url('./../../fonts/SuperMario.ttf');
}

</style>
