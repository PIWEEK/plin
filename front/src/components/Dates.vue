<template>
  <b-modal id="modal-dates" centered  size="lg" scrollable title="Cambiar fechas" style="height: 50rem">
      <b-container style="height: 20rem">
        <b-form>
          <b-form-group
            id="input-group-address"
            label="Fechas"
            label-for="input-date"
          >
            <b-row>
              <b-col>
                <b-form-datepicker
                  :date-format-options="{ year: '2-digit', month: '2-digit', day: '2-digit', weekday: 'narrow' }"
                  locale="es"
                  placeholder="Fecha inicial"
                  id="initial-date"
                  v-model="$store.state.currentTrip.from_date"
                  class="mb-2"
                  :disabled="noDates"/>
              </b-col>
              <b-col>
                <b-form-datepicker
                  :date-format-options="{ year: '2-digit', month: '2-digit', day: '2-digit', weekday: 'narrow' }"
                  locale="es"
                  placeholder="Fecha de fin"
                  id="end-date"
                  v-model="$store.state.currentTrip.to_date"
                  class="mb-2"
                  :disabled="noDates"/>
                </b-col>
              <b-col class="my-auto">
                <b-form-checkbox
                  id="checkbox-no-dates"
                  v-model="noDates"
                  name="checkbox-no-dates"
                >
                  Aún no sé fechas
                </b-form-checkbox>
              </b-col>
            </b-row>
          </b-form-group>



        </b-form>
      </b-container>

      <template #modal-footer="{ cancel}">
        <!-- Emulate built in modal footer ok and cancel button actions -->
        <b-button size="sm" variant="outline-secondary" @click="cancel()">
          Cerrar
        </b-button>
        <b-button size="sm" @click="updateTrip()">
          Guardar cambios
        </b-button>
      </template>
    </b-modal>
</template>

<script>

export default {
  name: "Dates",
  components: {
  },
  data() {
    return {
      noDates: this.$store.state.currentTrip.from_date == null
    }
  },
  computed: {
    validForm: function() {
      if (this.noDates) {
        return true;
      }
      return this.$store.state.currentTrip.from_date && this.$store.state.currentTrip.to_date;
    }
  },
  methods: {

    updateTrip: async function() {

      var trip = {
        "duration": duration,
        "from_date": this.$store.state.currentTrip.from_date,
        "to_date": this.$store.state.currentTrip.to_date
      }
      if (this.noDates) {
        trip["from_date"] = null;
        trip["to_date"] = null;
      }

      var duration = this.$store.state.currentTrip.duration
      if (this.$store.state.currentTrip.from_date && this.$store.state.currentTrip.to_date) {
        const dt1 = new Date(this.$store.state.currentTrip.from_date);
        const dt2 = new Date(this.$store.state.currentTrip.to_date);
        duration = Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24));
      }



      const id = this.$store.state.currentTrip.id;

      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("updateTrip", {tripId:id, data:trip});
      await this.$store.dispatch("fetchTrip");
      this.$bvModal.hide('modal-dates');
      this.$store.commit("SET_SHOWSPINNER", false);
    }
  }
};
</script>

<style lang="scss" scoped>
  .create-button {
    margin-top: 40px;
  }
</style>