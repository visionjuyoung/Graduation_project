package kr.psk.kpu.imagetestflask

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.firepush.Fire
import com.google.firebase.iid.FirebaseInstanceId
import kotlinx.android.synthetic.main.activity_main.*
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.*


class MainActivity : AppCompatActivity() {

    lateinit var myRetrofit : Retrofit
    lateinit var myRetrofitAPI : RetrofitAPI // custom
    lateinit var myCallImage : retrofit2.Call<ResponseBody>
    lateinit var pushtoken : String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        var serverkey = "AAAAOYtUnXk:APA91bGSzC-3SOeVbEgiu3uV_udbcGYk2vzKW9UpCdEghFsMrQBzoePYinKJBrU9HHWeL0EvMRhdarnXcE3rHxtQWqJt5z4EAKJecSCtVL1rHMNTDKQQq1eM3XbZZrEgLHDkx36p3wT2"
        Fire.init(serverkey)
        pushtoken = FirebaseInstanceId.getInstance().token.toString()
        Log.d("dd123",pushtoken)
        setContentView(R.layout.activity_main)




        setRetrofit()
        // 먼저 파일명을 가져와야 함

        button.setOnClickListener{
            Log.d("dd","1")
            Fire.create()
                .setTitle("TITLE HERE")
                .setBody("BODY HERE")
                .setCallback { pushCallback, exception ->
                    //get response here
                }
                .toIds("eBAOp5UUQxiuA6F9NsKc5T:APA91bGomx0X63bpVmgoeLlVSfN-YJ4U6EeW_xlnVow0QrtuZQGuaOScLzXcmrRDo8n8ItoRMgn-T48ntTINPRIc8le20IIV_9GQY_-jlibIGHwblXiQ4Vx5Htu2YaehJLJt4e3CHTcQ").push()
            Log.d("dd","2")
            callImage()
        }
    }

    private fun setRetrofit(){
        myRetrofit = Retrofit
            .Builder()
            .baseUrl(getString(R.string.baseUrl))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        myRetrofitAPI = myRetrofit.create(RetrofitAPI::class.java)
    }

    private fun callImage(){
        myCallImage = myRetrofitAPI.getImage("http://221.147.198.248:5000/static/images/bends.jpg")
        myCallImage.enqueue(myRetrofitCallback)
    }

    private val myRetrofitCallback = (object : retrofit2.Callback<ResponseBody>{
        override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
            textView.text = "이미지 업로드 에러" + t.message.toString()
        }

        override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
            var inputS : InputStream = response.body()!!.byteStream()
            var bmp : Bitmap = BitmapFactory.decodeStream(inputS)
            imageView.setImageBitmap(bmp)
        }
    })
}