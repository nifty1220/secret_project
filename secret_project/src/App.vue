<template>
  <LoginPage v-if="showLoginPage" @continueSiteSelectionPage="openSiteSelection" @retrieveUserData="loadUserData"/>
  <SiteSelectionPage v-if="showSiteSelectionPage" @showSelectedPage="openSelectedPage"/>
  <AliasPage v-if="showAliasPage" @backToPageSelection="openSiteSelection" :user_id="current_user_id" :user_settings="fetched_user_settings" :user_alias_sales="fetched_user_alias_sales"/>
  <StockxPage v-if="showStockxPage" @backToPageSelection="openSiteSelection" :user_id="current_user_id" :user_settings="fetched_user_settings"/>
  <SettingsPage v-if="showSettingsPage" @backToPageSelection="openSiteSelection" @retrieveUserData="loadUserData" :user_id="current_user_id" :user_settings="fetched_user_settings"/>
</template>

<script>

import LoginPage from './components/login_page.vue'
import SiteSelectionPage from './components/site_selection_page.vue'
import AliasPage from './components/alias.vue'
import StockxPage from './components/stockx.vue'
import SettingsPage from './components/settings_page.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    LoginPage,
    SiteSelectionPage,
    AliasPage,
    StockxPage,
    SettingsPage,
    },
    data() {
        return{
            showLoginPage: true,
            showSiteSelectionPage: false,
            showAliasPage: false,
            showStockxPage: false,
            showSettingsPage: false,

            fetched_user_settings: {},
            fetched_user_alias_sales: {},
            fetched_user_stockx_sales: {},

            current_user_id: null
        }
    },
    methods: {
        openSiteSelection() {
            this.showLoginPage = false
            this.showSiteSelectionPage = true
            this.showAliasPage = false
            this.showStockxPage = false
            this.showSettingsPage = false
        },
        openSelectedPage(page){
            if(page == "stockx") {
                this.showSiteSelectionPage = false
                this.showAliasPage = false
                this.showStockxPage = true
                this.showSettingsPage = false
            } else if (page == "alias") {
                this.showSiteSelectionPage = false
                this.showAliasPage = true
                this.showStockxPage = false
                this.showSettingsPage = false
            } else if (page == "settings") {
                this.showSiteSelectionPage = false
                this.showAliasPage = false
                this.showStockxPage = false
                this.showSettingsPage = true
            }
        },
        loadUserData(id) {

            this.current_user_id = id

            axios({
                    method: "GET",
                    url: 'http://10.0.0.9:5000/get_user_data',
                    data: {},
                    headers: {
                        "Content-Type": "application/json",
                        "user_id": id
                    },
                })
                .then((response) => {
                    this.fetched_user_settings = response.data["user_settings"]
                    this.fetched_user_alias_sales = response.data["user_alias_sales"]
                    this.fetched_user_stockx_sales = response.data["user_stockx_sales"]
                });
        }
    }
}

</script>

<style>

body {
    background-color: #1a1621;
}

#app {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    margin-top: 60px;
    height: 750px;
}

input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: none;
}

</style>
