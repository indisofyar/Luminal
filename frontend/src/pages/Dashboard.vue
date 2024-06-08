<template>
  <div class="p-8" v-if="transactions.length > 0">
    <div class="flex w-full gap-4 items-center">
      <div class="text-xl font-bold" v-if="transactions">
        {{ transactions[0].address.name }}
      </div>
      <div class="bg-slate-800 rounded-xl p-4">
        {{ transactions[0].address.address }}
      </div>
    </div>
    <section class="grid grid-cols-12 mt-8 gap-4">

      <div class="card col-span-4">
        <div class="card-title">Average Transaction Fee</div>
        <div class="text-xl"> {{ avgTran }}</div>
      </div>
      <div class="card col-span-4">
        <div class="card-title">Daily active addresses</div>
        <div class="text-xl"> {{ avgTran }}</div>
      </div>
      <div class="card col-span-4">
        <div class="card-title">Average Transaction Fee</div>
        <div class="text-xl"> {{ avgTran }}</div>
      </div>
      <div class="card h-[500px] col-span-6">
        <div class="card-title">User Journey</div>
        <Bar :data="data" :options="options"/>
      </div>

    </section>
    <!--    {{transactions}}-->
  </div>
</template>

<script>

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import {Bar} from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: "Dashboard",
  components: {Bar},
  data() {
    return {
      name: null,
      loaded: false,
      transactions: [],
      avgTran: null,
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      data: {
        labels: [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December'
        ],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
          }
        ]
      }
    }
  },
  methods: {
    getData() {
      const vm = this;
      this.$axios.get('/api/address/0x017E26DB707f62Ba3ce4641FFe2C7a109B780df1/').then((res) => {
        console.log(res.data)
        vm.avgTran = res.data.average_gas_fee
        vm.transactions = res.data.transactions
      })
    },
    getAddresses() {
      const vm = this;
      this.$axios.get('/api/address/all/').then((res) => {
        console.log(res.data)
        vm.avgTran = res.data.average_gas_fee
        vm.transactions = res.data.transactions
      })
    }
  },
  created() {
    this.getData();
    this.getAddresses();
  },

}
</script>

<style scoped>

</style>