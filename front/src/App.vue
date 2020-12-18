<template>
  <div id="app">
    <b-container :class="!hasUser || $route.meta.hideNavigationBar ? 'empty' : ''">
      <b-container v-if="hasUser && !$route.meta.hideNavigationBar">
        <b-navbar toggleable="lg" type="dark" variant="white">
          <b-navbar-brand href="/home">
            <b-img src="/logo.png" alt="Plin" style="height: 30px; margin-right: 1rem"></b-img>
            Plin
          </b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" is-nav>
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <!--
              <b-nav-form>
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
              </b-nav-form>
              -->

              <b-nav-item-dropdown right no-caret>
                <!-- Using 'button-content' slot -->
                <template #button-content>
                  <span class="text-info name">{{ $store.state.currentUser.name }}</span>
                  <b-img  rounded="circle" :src="gravatarUrl"/>
                </template>
                <!--<b-dropdown-item href="#">Profile</b-dropdown-item>-->
                <b-dropdown-item href="#" v-on:click="singOut">Salir</b-dropdown-item>
              </b-nav-item-dropdown>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </b-container>
      <router-view />
    </b-container>
    <div v-if="showSpinner" style="position: absolute; top:0; left:0; width: 100%; height: 100%; z-index: 100000; background-color: rgba(255,255,255,0.5);">
      <b-spinner label="Loading..." style="position: absolute;top: 50%; left: 50%"></b-spinner>
    </div>
  </div>
</template>

<script>
    export default {
      computed: {
        hasUser(){
          return this.$store.state.currentUser.username != null;
        },
        showSpinner(){
          return this.$store.state.showSpinner;
        },
        gravatarUrl() {
          const md5 = require('md5');
          console.log("gravatarUrl", this.$store.state.currentUser)
          return `https://www.gravatar.com/avatar/${md5(this.$store.state.currentUser.email || '')}?s=30`;
        }
      },
      methods: {
        singOut(){
          this.$store.commit("SET_TRIPS", {});
          this.$store.commit("SET_CURRENTTRIP", {});
          this.$store.commit("SET_CURRENTUSER", {});
          this.$router.push("/");
        }
      }
    }
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

#app {
  font-family: 'Nunito', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.empty {
  padding-top: 40px;
}

.name {
  padding-right: 14px;
}
</style>
