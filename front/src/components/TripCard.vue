<template>
  <b-card
    style="width: calc(25% - 10px); margin: 5px; height:20rem; cursor: pointer"
    class="image"
    v-on:click="selectTrip"
    top
    :img-src="url_picture"
    img-alt="Image"
    :title="title"
  >

    <b-card-text>
    <!--
      <h4 style="height: 4rem">
        {{ title }}
      </h4>
      <div>
    -->
        <span v-if="start">Del {{ start }} </span>
        <span v-if="end">al {{ end }} </span>
        <div>
          {{ duration }} días
        </div>
    <!--
      </div>
    -->
    </b-card-text>
  </b-card>
</template>

<script>
    export default {
      props: ["id", "title", "url_picture", "start", "end", "duration"],
      methods: {
        selectTrip: function () {
          this.$store.commit('SET_CURRENTTRIP', {id:this.id, title: this.title, url_picture: this.url_picture});
          this.$router.push("/trip");
        }
      }
    }
</script>

<style lang="scss" scoped>
.image img {
  height: 140px;
  object-fit: cover;
}
</style>