import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    trips: [],
    displayTrips: [],
    rows: 0,
    showSpinner: false,
    currentTrip: {},
    currentUser: {"name": null},
    fakeData: true
  },
  mutations: {
    SET_TRIPS(state, trips) {
      state.trips = trips;
    },
    SET_CURRENTTRIP(state, currentTrip) {
      state.currentTrip = currentTrip;
    },
    SET_CURRENTUSER(state, currentUser) {
      state.currentUser = currentUser;
    }
  },
  actions: {
    async fetchData(context, url) {
      return new Promise(resolve => {
        setTimeout(async () => {
          const res = await fetch(url, {
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
      const myJson = await dispatch("fetchData", state.fakeData ? "fake/trips.json" : "http://localhost:8000/api/trips/");
      commit("SET_TRIPS", myJson);
      return myJson;
    },
    async fetchTrip({ dispatch, commit, state }) {      
      const url = "http://localhost:8000/api/trips/" + state.currentTrip.id;      
      const myJson = await dispatch("fetchData", state.fakeData ? "fake/trip.json" : url)
      commit("SET_CURRENTTRIP", myJson);
      return myJson;
    },
    async login({dispatch, state}, body) {
      if (state.fakeData){
        return await dispatch("fetchData", "fake/login.json")
      } else {
        return new Promise(resolve => {
          setTimeout(async () => {
            const res = await fetch(
              "http://localhost:8000/api/token/", 
              {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                },
                body: body
              });
            const val = await res.json();
            resolve(val);
          }, 1000);
        });
      }
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
