package kr.psk.kpu.imagetestflask

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.tasks.OnCompleteListener
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        FirebaseInstanceId.getInstance().instanceId
            .addOnCompleteListener(OnCompleteListener { task ->
                if (!task.isSuccessful) {
                    Log.w("FCM Log", "getInstanceId failed", task.exception)
                    return@OnCompleteListener
                }
                val token = task.result!!.token
                Log.d("FCM Log", "FCM 토큰: $token")
                Toast.makeText(this@MainActivity, token, Toast.LENGTH_SHORT).show()
            })


        setRetrofit()
        // 먼저 파일명을 가져와야 함

        button.setOnClickListener{
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