

import android.content.Intent
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.widget.Toast
import com.facebook.*
import com.google.android.gms.auth.api.Auth
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import kotlinx.android.synthetic.main.activity_login.*
import com.facebook.appevents.AppEventsLogger;
import com.facebook.login.LoginManager
import com.facebook.login.LoginResult
import com.google.firebase.auth.FacebookAuthProvider
import java.security.MessageDigest
import java.security.NoSuchAlgorithmException
import java.util.*


class LoginActivity : AppCompatActivity() {
    var auth: FirebaseAuth? = null // 로그인을 관리해주는 클래스 FirebaseAuth
    var googleSignInClient: GoogleSignInClient?=null
    var GOOGLE_LOGIN_CODE=9001 // 임의 숫자 넣으면 됨
    var callbackManager:CallbackManager?=null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        auth = FirebaseAuth.getInstance() //auth 초기화

        email_login_button.setOnClickListener {
            createAndLoginEmail()
        }
        google_sign_in_button.setOnClickListener {
            googleLogin()
        }

        facebook_login_button.setOnClickListener{
            facebookLogin()
        }

        // 구글 시작하기 전에 세팅해주는 것
        var gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))//Client id= 구글로그인에 접근할 수 있도록 허가해주는 아이디 키값. 얘가 있어야 구글 로그인에 접근 가능 (일종의 로그인 인증키)
            .requestEmail()
            .build() // 조립 완성됐다는 뜻
        googleSignInClient= GoogleSignIn.getClient(this,gso) // 구글 로그인하는 클래스 완성됨!


        callbackManager= CallbackManager.Factory.create() // 초기화
    }

    fun createAndLoginEmail() {
        auth?.createUserWithEmailAndPassword(
            email_edittext.text.toString(),
            password_edittext.text.toString()
        )?.addOnCompleteListener { task -> //파라미터를 받아옴
            if (task.isSuccessful) {
                //Toast.makeText(this, "아이디 생성이 완료되었습니다.", Toast.LENGTH_LONG).show()
                moveMainPage(auth?.currentUser)
            } else if (task.exception?.message.isNullOrEmpty()) {
                // 익셉션에 메시지가 있을 경우 메세지 출력
                //isnullorempty 대신 !=null 해도 됨
                Toast.makeText(this, task.exception?.message, Toast.LENGTH_LONG).show()
            } else {
                // 로그인임. 아이디&비번도 있고, 익셉션도 없다면 로그인!
                signinEmail()
            }

        }
    }

    fun signinEmail() {
        auth?.signInWithEmailAndPassword(
            email_edittext.text.toString(),
            password_edittext.text.toString()
        )
            ?.addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    //Toast.makeText(this, "로그인이 성공했습니다.", Toast.LENGTH_LONG).show()
                    moveMainPage(auth?.currentUser)//auth는 로그인이 성공하면 유저에 대한 정보를 가지게 된다.
                } else {
                    Toast.makeText(this, task.exception?.message, Toast.LENGTH_LONG).show()
                }

            }
    }

    fun moveMainPage(user: FirebaseUser?) {
        if (user != null) {
            //유저가 있을 경우 다음 페이지로 넘어감
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }

    }

    fun googleLogin() {
        var signInIntent=googleSignInClient?.signInIntent
        startActivityForResult(signInIntent,GOOGLE_LOGIN_CODE)
    }

    fun facebookLogin(){
        LoginManager.getInstance()
            .logInWithReadPermissions(this, Arrays.asList("public_profile","email"))
        LoginManager
            .getInstance()
            .registerCallback(callbackManager,object:FacebookCallback<LoginResult>{
                override fun onSuccess(result: LoginResult?) {
                    println("onSuccess")
                    handleFacebookAccessToken(result?.accessToken)
                }

                override fun onCancel() {
                    println("onCancel")

                }

                override fun onError(error: FacebookException?) {
                    println("onError")

                }

            })
    }

    fun handleFacebookAccessToken(token:AccessToken?){
        var credential=FacebookAuthProvider.getCredential(token?.token!!)
        auth?.signInWithCredential(credential)!!.addOnCompleteListener {
            task->
            println("task"+task.isSuccessful)
            Log.d("페이스북",task.isSuccessful.toString())
        }.addOnFailureListener{
            exception ->
            println("exception"+exception.message)
        }
    }

    fun firebaseAuthWithGoogle(account:GoogleSignInAccount){
        // 인증서를 먼저 만들어줘야 함
        var credential=GoogleAuthProvider.getCredential(account.idToken,null)
        auth?.signInWithCredential(credential)

    }
    // 결과값을 받는 함수, 구글 버튼 누르고 사용자의 계정을 선택하면 그 결과값이 넘어옴
    // 사용자의 계정을 선택하는 창이 꺼졌을 때 이전 액티비티 (로그인 액티비티) 에게 값이 넘어가고
    // 그 값이 firebase에 갱신되도록 한다.
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        callbackManager?.onActivityResult(requestCode,resultCode,data)

        // 넘어온 사용자의 정보를 가공
        if(resultCode==GOOGLE_LOGIN_CODE ){
            var result= Auth.GoogleSignInApi.getSignInResultFromIntent(data)
            if(result.isSuccess){
                // 구글 로그인에 성공했을 경우 파이어베이스에게 값 넘겨줘야 함 - firebaseAuthWithGoogle
                var account=result.signInAccount
                firebaseAuthWithGoogle(account!!)
            }
        }
    }





}