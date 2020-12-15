<template>
<div class="day">
  <div>{{ currentDay.name}}</div>
  <plan-card
          :name="plan.name"
          :image="plan.image"
          :id="plan.id"
          v-for="plan in currentDay.plans"
          :key="plan.id"
        ></plan-card>
</div>
</template>

<script>
    import PlanCard from '@/components/PlanCard.vue'

    export default {
      components: {
        'plan-card': PlanCard
      },
      props: ["currentDay"]
    }
</script>

<style lang="scss" scoped>
.day {
  background-color: lightgray;
  border: 1px solid blue;
  display: inline-block;
  height: 100%;
  width: 20rem;
}

</style>