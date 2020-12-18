<template>
  <b-container>
    <b-container class="create-trip">
      <h1 class="title">¡Haz las maletas!</h1>
      <manage-trip />
    </b-container>

  <b-row>
    <h1 style="margin-top: 5rem">Próximos Viajes</h1>
    <trips />
    <h1 style="margin-top: 5rem">Viajes pasados</h1>
    <trips />
  </b-row>
  </b-container>
</template>

<script>
import ManageTrip from '@/components/ManageTrip.vue';
import Trips from '@/components/Trips.vue';

export default {
  name: "Home",
  components: {
    'manage-trip': ManageTrip,
    'trips': Trips
  },
  data() {
    return {
      place: null,
      initialDate: null,
      endDate: null,
      noDates: false,
      urlPicture: `${window.location.origin}/images/default-trip-${1 + Math.floor(Math.random() * Math.floor(9))}.png`,
      duration: null,
      places: []
    }
  },
  computed: {
    validForm: function() {
      if (!this.place) {
        return false
      }
      if (this.noDates) {
        return true;
      }
      return this.initialDate && this.endDate;
    }
  },
  async mounted() {
    if (! this.$store.state.currentUser.token){
      this.$router.push("/");
    } else if (! this.$store.state.currentUser.id){
      await this.getUserInfo();
    }
  },
  methods: {
    async getUserInfo() {
      const userInfo = await this.$store.dispatch("me", JSON.stringify(this.form));
      var currentUser = this.$store.state.currentUser;
      currentUser["name"] = userInfo.first_name;
      currentUser["id"] = userInfo.id;
      this.$store.commit("SET_CURRENTUSER", currentUser);
    }
  }
};
</script>

<style lang="scss" scoped>
  .title {
    color: #FAFAFA;
    font-size: 86px;
    font-weight: bold;
  }

  .create-button {
    margin-top: 40px;
  }

  .title {
    color: #FAFAFA;
    font-size: 86px;
    font-weight: bold;
  }

  .create-trip {
     background-image: url("/create_trip_bg.png");
     background-size: cover;
     padding: 30px 85px 60px 85px;
  }
</style>
