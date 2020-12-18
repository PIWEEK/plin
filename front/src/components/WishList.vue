<template>
  <div>
    <b-button block variant="primary" @click="showModal()">
      + Nuevo plan
    </b-button>
    <div
      style="width: 100%; height: 40rem"
      class="wishlist radius-lg drop-zone"
      @drop='onDrop($event, 1)' 
      @dragover.prevent
      @dragenter.prevent
      >
        <plan-card
          class="shadow-sm"
          :plan="plan"
          v-for="plan in $store.state.currentTrip.wishlist"
          v-on:plan_drop_on_child="planDropOnChild"
          v-on="$listeners"
          :key="plan.id">
        </plan-card>
    </div>
  </div>
</template>

<script>
  import PlanCard from '@/components/PlanCard.vue';
  
  export default {
    components: {
      'plan-card': PlanCard
    },
    data() {
      return {        
      }
    },
    methods: {
      showModal: function() {
        this.$emit('create_plan');
      },
      
      async movePlan(planId, beforePlan){
          this.$store.commit("SET_SHOWSPINNER", true);
          await this.$store.dispatch("movePlan", {"planId": planId, "dayId": null, "beforePlan": beforePlan});
          await this.$store.dispatch("fetchTrip");
          this.$store.commit("SET_SHOWSPINNER", false);
        },      
      onDrop (evt) {
        const planId = evt.dataTransfer.getData('planId');
        console.log("onDrop "+planId);
        this.movePlan(planId);
      },
      planDropOnChild (planId, beforePlan) {    
        this.movePlan(planId, beforePlan);
      }
    }
  }
</script>

<style lang="scss" scoped>
  .wishlist {
    border-radius: 5px;
    background-color: #EDEEFF;
    margin-top: 0.5rem;
    padding: 10px 1px;
    width: 100%;
  }
</style>