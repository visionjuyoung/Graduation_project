package kr.psk.kpu.imagetestflask

import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Url

interface RetrofitAPI {
    @GET
    fun getImage(@Url fileUrl:String) : Call<ResponseBody>
}