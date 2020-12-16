import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    trips: [],
    displayTrips: [],
    rows: 0,
    currentTrip: {},
    currentUser: {"name": null},
    showSpinner: false,
    fakeData: false
  },
  mutations: {
    INITIALIZE_STORE(state) {
      if (localStorage.getItem('state')) {
        const localStorageState = JSON.parse(localStorage.getItem('state'));
        state.trips = localStorageState.trips;
        state.displayTrips = localStorageState.displayTrips;
        state.rows = localStorageState.rows;
        state.showSpinner = false;
        state.currentTrip = localStorageState.currentTrip;
        state.currentUser = localStorageState.currentUser;
      }
    },
    SET_TRIPS(state, trips) {
      state.trips = trips;
      localStorage.setItem('state', JSON.stringify(state));
    },
    SET_CURRENTTRIP(state, currentTrip) {
      state.currentTrip = currentTrip;
      localStorage.setItem('state', JSON.stringify(state));
    },
    SET_CURRENTUSER(state, currentUser) {
      state.currentUser = currentUser;
      localStorage.setItem('state', JSON.stringify(state));
    },
    SET_SHOWSPINNER(state, showSpinner) {
      state.showSpinner = showSpinner;
      localStorage.setItem('state', JSON.stringify(state));
    }
  },
  actions: {
    async fetchData(context, data) {
      return new Promise(resolve => {
        setTimeout(async () => {
          const res = await fetch(data.url, {
            method: data.method,
            body: data.body,
            headers: {
              'Authorization': 'JWT '+ context.state.currentUser.token,
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          });
          const val = await res.json();
          resolve(val);
        }, 1000);
      });
    },
    async fetchTripsList({ dispatch, commit, state }) {
      const myJson = await dispatch("fetchData",
        state.fakeData ? {url:"fake/trips.json", method:"GET", body: null} : {url:"http://localhost:8000/api/trips/", method:"GET", body: null});
      commit("SET_TRIPS", myJson);
      return myJson;
    },
    async fetchTrip({ dispatch, commit, state }) {
      const url = "http://localhost:8000/api/trips/" + state.currentTrip.id;
      const myJson = await dispatch("fetchData", state.fakeData ? {url:"fake/trip.json", method:"GET", body: null} : {url: url, method:"GET", body: null});
      commit("SET_CURRENTTRIP", myJson);
      return myJson;
    },
    async movePlan({ dispatch, state }, data) {
      if (!state.fakeData) {
        const url = "http://localhost:8000/api/trips/" + state.currentTrip.id + "/plans/" + data.planId +"/";
        await dispatch("fetchData", {url: url, method:"PATCH", body: JSON.stringify({"day": data.dayId})});
      }
    },
    async createTrip({ dispatch, state }, newTrip) {
      if (!state.fakeData) {
        const url = "http://localhost:8000/api/trips/";
        await dispatch("fetchData", {url: url, method:"POST", body: JSON.stringify(newTrip)});
      }
    },
    async createPlan({ dispatch, state }, newPlan) {
      if (!state.fakeData) {
        const url = "http://localhost:8000/api/trips/" + state.currentTrip.id + "/plans/";
        await dispatch("fetchData", {url: url, method:"POST", body: JSON.stringify(newPlan)});
      }
    },
    async login({dispatch, state}, body) {
      const myJson = await dispatch("fetchData", state.fakeData ? {url:"fake/login.json", method:"GET", body: null} : {url: "http://localhost:8000/api/token/", method:"POST", body: body});
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
