<template>
  <b-card
    style="width: calc(25% - 20px); margin: 10px; height:15rem; cursor: pointer"
    class="image shadow-sm"
    v-on:click="selectTrip"
    top
    :img-src="url_picture"
    img-alt="Image"
  >
    <b-card-title>{{title}}</b-card-title>

    <b-card-text>
      <span class="font-weight-bold" v-if="start">{{ prettyPrintDate(start) }} </span>
      <span class="font-weight-bold" v-if="end">- {{ prettyPrintDate(end) }} </span>
      ({{ duration }} días)
    </b-card-text>
  </b-card>
</template>

<script>
    import moment from 'moment';

    export default {
      props: ["id", "title", "url_picture", "start", "end", "duration"],
      methods: {
        selectTrip: function () {
          this.$store.commit('SET_CURRENTTRIP', {id:this.id, title: this.title, url_picture: this.url_picture});
          this.$router.push("/trip");
        },
        prettyPrintDate: function (d) {
          moment.locale('es');
          return moment(d).format("D MMM");
        }
      }
    }
</script>

<style lang="scss" scoped>
.image img {
  height: 160px;
  object-fit: cover;
}

.card {
  text-align: center;
}

.card-body {
  padding: 0.75rem 1.25rem;
}

.card-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 4px;
}
</style>