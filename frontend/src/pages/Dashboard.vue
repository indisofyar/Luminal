<template>
  <div class="p-8">
    <div class="flex w-full gap-4 items-center">
      <div class="text-xl font-bold">
        {{transactions[0].address.name}}
      </div>
      <div class="bg-slate-800 rounded-xl p-4">
      {{transactions[0].address.address}}
      </div>
    </div>
<!--    {{transactions}}-->
  </div>
</template>

<script>


export default {
  name: "Dashboard",
  data() {
    return {
      name: null,
      loaded: false,
      transactions: [],
    }
  },
  methods: {
    getData() {
      const vm = this;
      this.$axios.get('/api/address/0x017E26DB707f62Ba3ce4641FFe2C7a109B780df1/').then((res) => {
        vm.transactions = res.data
      })
    }
  },
  created() {
    this.getData()
  }
}
</script>

<style scoped>

</style>