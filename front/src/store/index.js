import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    trips: [],
    displayTrips: [],
    rows: 0,
    showSpinner: false,
    currentTrip: {}
  },
  mutations: {
    SET_TRIPS(state, trips) {
      state.trips = trips;
    },
    SET_CURRENTTRIP(state, currentTrip) {
      state.currentTrip = currentTrip;
    }
  },
  actions: {
    async fetchData(context, url) {
      return new Promise(resolve => {
        setTimeout(async () => {
          const res = await fetch(url);
          const val = await res.json();
          resolve(val);
        }, 1000);
      });
    },
    async fetchTripsList({ dispatch, commit }) {
      const myJson = await dispatch("fetchData", "trips.json");
      commit("SET_TRIPS", myJson);
      return myJson;
    },
    async fetchTrip({ dispatch, commit }) {
      const myJson = await dispatch("fetchData", "trip.json");
      commit("SET_CURRENTTRIP", myJson);
      return myJson;
    }
  },
  getters: {
    getTrips(state) {
      return state.trips;
    },
    getCurrentTrip(state) {
      return state.currentTrip;
    }
  },
  modules: {}
});