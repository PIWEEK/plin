<template>
  <b-container>
    <div class="d-flex align-items-center header" :style="headerImg">
      <b-container>
        <div class="w-100">
          <h1
            class="editTitle"
            contenteditable="true"
            id="trip-title"
            v-text="editTitle"
            @blur="onTitleEdit"
            @keydown.enter="endTitleEdit"
          />
        </div>
      </b-container>
    </div>
    <b-container>
      <b-dropdown size="lg"  variant="link" toggle-class="text-decoration-none" no-caret>
        <template #button-content>
           <b-icon-gear variant="dark"/>
        </template>
        <!--<b-dropdown-item href="#">Duplicar viaje</b-dropdown-item>-->
        <b-dropdown-item-button @click="deleteTrip()">Borrar viaje</b-dropdown-item-button>
        <!--<b-dropdown-item href="#">Mover todos los planes al listado</b-dropdown-item>-->
      </b-dropdown>

    </b-container>

    <b-row class="text-center">
      <b-col cols="3">
        <wishlist></wishlist>
      </b-col>
      <b-col cols="9">
      <week></week>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import WishList from '@/components/WishList.vue'
import Week from '@/components/Week.vue'
// import {_} from 'vue-underscore';

export default {
  name: "Trip",
  async mounted() {
    this.getRecords();
  },
  components: {
    'wishlist': WishList,
    'week': Week
  },
  data() {
    return {
      editTitle: this.$store.state.currentTrip.title
    };
  },
  methods: {
    onTitleEdit(evt){
      var src = evt.target.innerText
      this.editTitle = src
    },
    endTitleEdit(){
      this.$el.querySelector('.editTitle').blur()
      this.$store.dispatch("updateTrip", {tripId: this.$store.state.currentTrip.id, data: { title: this.editTitle }});
    },
    async deleteTrip() {
      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("deleteTrip", this.$store.state.currentTrip.id);
      await this.$store.dispatch("fetchTripsList");
      this.$router.push("/home");
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    async getRecords() {
      if (this.$store.state.currentUser.token === undefined){
        this.$router.push("/");
      }
      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("fetchTrip");
      this.$store.commit("SET_SHOWSPINNER", false);
    }
  },
  computed: {
      headerImg () {
        return "background-image: url('" + this.$store.state.currentTrip.url_picture + "')";
      }
    },
};
</script>

<style lang="scss" scoped>

.header {
  color: white;
  background-color: #cccccc; /* Used if the image is unavailable */
  height: 8rem; /* You must set a specified height */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  background-size: cover; /* Resize the background image to cover the entire container */
}

</style>