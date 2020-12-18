<template>
  <b-container>
    <div class="d-flex align-items-center header position-relative" :style="headerImg" @mouseover="hoverImage = true" @mouseleave="hoverImage = false" >
      <div v-if="hoverImage" class="position-absolute"  style="top: 10px; right: 10px">
        <b-img class="icon-update-url-picture" width="44px" style="padding: 8px" src="/edit.png" @click="$bvModal.show('modal-update-url-picture')"></b-img>
      </div>

      <b-container fluid>
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
    <b-container fluid style="box-shadow: 0px 2px 2px lightgray; margin-bottom:0.3rem">
      <b-row align-v="center">
        <b-col style="padding: 0">
          <b-dropdown size="lg"  variant="link" toggle-class="text-decoration-none" no-caret>
            <template #button-content>
              <b-icon-gear variant="dark"/>
            </template>
            <!--<b-dropdown-item href="#">Duplicar viaje</b-dropdown-item>-->
            <b-dropdown-item-button @click="deleteTrip()">Borrar viaje</b-dropdown-item-button>
            <b-dropdown-item-button @click="resetTrip()">Mover todos los planes al listado</b-dropdown-item-button>
          </b-dropdown>
        </b-col>
        <b-col style="text-align: center">
            <b-icon-plus-circle variant="dark" style="width: 1.5rem; height: 1.5rem; margin-right: 1rem" v-b-tooltip.hover title="Añadir un día"/>
            <b-icon-calendar-3 @click="openEditTrip"  variant="dark" style="width: 1.5rem; height: 1.5rem; margin-right: 1rem; cursor:pointer" v-b-tooltip.hover title="Editar fechas y número de días"/>
            <b-icon-house-door variant="dark" style="width: 1.5rem; height: 1.5rem;" v-b-tooltip.hover title="Añadir o editar alojamientos"/>
        </b-col>
        <b-col style="text-align: right">
          <b-img :src="gravatar(member.email)" style="height:2rem;margin-right:1rem" rounded="circle" v-for="member in this.$store.state.currentTrip.members" :key="member.id"></b-img>
          <b-button variant="outline-primary" @click="openAddMember">Añadir acompañante</b-button>
        </b-col>
      </b-row>

    </b-container>

    <b-row class="text-center">
      <b-col cols="3">
        <wishlist v-on:edit_plan="editPlan" v-on:create_plan="createPlan" v-on:duplicate_plan="duplicatePlan"></wishlist>
      </b-col>
      <b-col cols="9">
      <week v-on:edit_plan="editPlan" v-on:duplicate_plan="duplicatePlan"></week>
      </b-col>
    </b-row>
    <plan ref="currentPlan"></plan>
    <b-modal id="modal-update-url-picture" centered  size="lg" scrollable title="Cambiar imagen" hide-footer>
      <b-form>
        <b-form-group
          id="input-group-url-picture"
          label="Url de la imagen"
          label-for="input-url-picture"
        >
          <b-form-input
            id="input-url-picture"
            v-model="editUrlPicture"
            placeholder="Copia la URL de la imagen aquí"/>
        </b-form-group>
        <b-button variant="primary" block @click="updateUrlPicture()">Aceptar</b-button>
      </b-form>
    </b-modal>

    <b-modal id="modal-add-member" centered  size="lg" scrollable title="Añadir acompañante" hide-footer>
      <b-form @submit="addMember">
        <b-form-group
          id="input-group-url-picture"
          label="Añade el email de tu acompañante"
          label-for="input-member-email"
        >
          <b-form-input
            type="email"
            id="input-member-email"
            v-model="memberEmail"
            placeholder="El acompañante debe estar registrado en Plín"/>
        </b-form-group>
        <b-button type="submit" variant="primary" block>Aceptar</b-button>
      </b-form>
    </b-modal>



    <dates />


  </b-container>
</template>

<script>
import WishList from '@/components/WishList.vue'
import Week from '@/components/Week.vue'
import Plan from '@/components/Plan.vue';
import Dates from '@/components/Dates.vue';

export default {
  name: "Trip",
  async mounted() {
    this.getRecords();
  },
  components: {
    'dates': Dates,
    'wishlist': WishList,
    'week': Week,
    'plan': Plan
  },
  data() {
    return {
      editTitle: this.$store.state.currentTrip.title,
      editUrlPicture: this.$store.state.currentTrip.url_picture,
      hoverImage: false,
      memberEmail: '',
    };
  },
  methods: {
    onTitleEdit(evt){
      var src = evt.target.innerText
      this.editTitle = src
    },
    endTitleEdit() {
      this.$el.querySelector('.editTitle').blur()
      this.$store.dispatch("updateTrip", {tripId: this.$store.state.currentTrip.id, data: { title: this.editTitle }});
    },
    updateUrlPicture() {
      this.$store.commit("SET_SHOWSPINNER", true);
      this.$store.dispatch("updateTrip", {tripId: this.$store.state.currentTrip.id, data: { url_picture: this.editUrlPicture }});
      this.$bvModal.hide('modal-update-url-picture');
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    openAddMember(){
      this.memberEmail = '';
      this.$bvModal.show('modal-add-member')
    },
    async addMember(event) {
      event.preventDefault();
      this.$store.commit("SET_SHOWSPINNER", true);
      const response = await this.$store.dispatch("addMember", {tripId: this.$store.state.currentTrip.id, data: { email: this.memberEmail }});
      this.$bvModal.hide('modal-add-member');

      if ("user not found" == response){
        this.$store.commit("SET_SHOWSPINNER", false);
        this.$bvModal.msgBoxOk("No se ha podido añadir al acompañante. ¿Seguro que está registrado en Plín?", {okVariant: "danger"})
      } else {
        await this.$store.dispatch("fetchTrip");
        this.$store.commit("SET_SHOWSPINNER", false);
      }

      return false;
    },
    async deleteTrip() {
      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("deleteTrip", this.$store.state.currentTrip.id);
      await this.$store.dispatch("fetchTripsList");
      this.$router.push("/home");
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    async resetTrip() {
      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("resetTrip", this.$store.state.currentTrip.id);
      await this.$store.dispatch("fetchTrip");
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    async getRecords() {
      if (this.$store.state.currentUser.token === undefined){
        this.$router.push("/");
      }
      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("fetchTrip");
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    editPlan (planJson) {
      const plan = JSON.parse(planJson);
      this.$refs.currentPlan.fillPlan(plan);
      this.$bvModal.show('modal-new-plan');
    },
    createPlan () {
      this.$refs.currentPlan.fillPlan(null);
      this.$bvModal.show('modal-new-plan');
    },
    async duplicatePlan (planJson) {
      this.$store.commit("SET_SHOWSPINNER", true);
      const plan = JSON.parse(planJson);
      await this.$refs.currentPlan.duplicatePlan(plan);
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    gravatar(email) {
      var md5 = require('md5');
      const hash = md5(email)
      return "http://www.gravatar.com/avatar/"+hash;
    },
    openEditTrip(){
      this.$bvModal.show('modal-dates');
    }
  },
  computed: {
      headerImg () {
        return `background-image: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%), url('${this.$store.state.currentTrip.url_picture}');`;
      }
    },
};
</script>

<style lang="scss" scoped>
  .header {
    color: white;
    background-color: #cccccc; /* Used if the image is unavailable */
    height: 10rem; /* You must set a specified height */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-size: cover; /* Resize the background image to cover the entire container */
  }

  .icon-update-url-picture{
    cursor: pointer;
  }

  h1 {
    font-weight: bolder;
    text-align: center;
  }
</style>