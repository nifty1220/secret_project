<template>
    <h1 id="page_selection_title"> Page Selection </h1>
    <div id="store_container">
        <div id="stockx_container" @click="openStockx()">
            <img id="stockx_image" src="./../assets/stockx.png">
            <p id="icon_label"> StockX </p>
        </div>
        <div id="alias_container" @click="openAlias()">
            <img id="alias_image" src="./../assets/alias.png">
            <p id="icon_label"> Alias </p>
        </div>
    </div>
    <div id="settings_container" @click="openSettings()">
        <img id="settings_image" src="./../assets/settings_icon.png">
        <br><br>
        <p id="settings_label" style="display:inline"> Settings </p>
    </div>
</template>

<script>
export default {
  name: 'SiteSelectionPage',
  emits: {
      showSelectedPage:null
  },
  data() {
      return {
      }
  },
  methods: {
      openStockx() {
          this.$emit("showSelectedPage", "stockx")
      },
      openAlias() {
          this.$emit("showSelectedPage", "alias")
      },
      openSettings() {
          this.$emit("showSelectedPage", "settings")
      },
  }
}
</script>


<style scoped>

#page_selection_title {
    font-family: SuperMario;
    src: url('./../../fonts/pixel.TTF');
    color: white;
    font-size: 400%;
}

#store_container {
    background-color: white;
}

#stockx_container {
    float: left;
    width: 10%;
    margin-left: 35%;
    margin-top: 5%;
}

#stockx_container:hover {
    cursor: pointer;
}

#stockx_image {
    width: 100%;
    border-radius: 30px;
    box-shadow: rgba(255, 255, 255, 0.4) 0px 0px 50px;
    border: 5px solid;
    border-color: black
}

#alias_container {
    float: right;
    width: 10%;
    margin-right: 35%;
    margin-top: 5%;
}

#alias_container:hover {
    cursor: pointer;
}

#alias_image {
    width: 100%;
    border-radius: 30px;
    box-shadow: rgba(0, 0, 0, 1) 0px 0px 50px;
    border: 4px solid;
    border-color: white
}

#settings_container {
    margin-top: 30%;
    margin-left: 46.25%;
    width: 7.5%;
    //background-color: red;
}

#settings_container:hover {
    cursor: pointer;
}

#settings_image {
    //border-color: rgba(51, 51, 51);
    -webkit-filter: drop-shadow(5px 5px 0 black) drop-shadow(-1px -1px 0 black);
    filter: drop-shadow(2px 2px 0 white) drop-shadow(-1px -1px 0 white);
}

#icon_label {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 200%;
    color: white;
    text-shadow: black 2.5px 2.5px;
}

#settings_label {
    font-family: Square;
    src: url('./../../fonts/Square.TTF');
    font-size: 200%;
    color: white;
    text-shadow: black 2.5px 2.5px;
}

h1 {
    text-shadow: black 7.5px 7.5px;
}

</style>
