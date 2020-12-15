<template>
<div class="wishlist">
  <plan-card
          :name="plan.name"
          :image="plan.image"
          :id="plan.id"
          v-for="plan in $store.state.currentTrip.wishlist"
          :key="plan.id"
        ></plan-card>
</div>
</template>

<script>
    import PlanCard from '@/components/PlanCard.vue'

    export default {
      components: {
        'plan-card': PlanCard
      }
    }
</script>

<style lang="scss" scoped>
.wishlist {
  background-color: lightblue;
  width: 100%;
  height: 300px;
  border: 1px solid black;
}

</style>