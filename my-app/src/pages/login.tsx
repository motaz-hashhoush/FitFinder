import { Link, useLocation } from "wouter"; // استورد useLocation
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { LogIn, Eye, EyeOff, Shield, Mail, Lock, Rocket } from "lucide-react";

import { FcGoogle } from "react-icons/fc";
import { AiFillApple } from "react-icons/ai";
import { FaMicrosoft } from "react-icons/fa";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const [, setLocation] = useLocation(); // setLocation

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    await new Promise((resolve) => setTimeout(resolve, 1500));

    console.log("Login:", { email, password });
    setIsLoading(false);

    //after successful login, redirect to dashboard
    setLocation("/dashboard");
  };

  return (
    <div className="min-h-screen flex  relative overflow-hidden">
      {/* Background Pattern */}
      {/* <div className="absolute inset-0 opacity-20">
        <div
          className="w-full h-full"
          style={{
            backgroundImage:
              "repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,182,193,0.3) 20px, rgba(255,182,193,0.3) 40px)",
          }}
        ></div>
      </div> */}

      {/* Left Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8 relative z-10">
        <div className="w-full max-w-md">
          {/* Logo */}
          <div className="mb-8">
            <div className="flex items-center space-x-2 mb-6">
              <div className="bg-blue-600 rounded-lg p-2">
                <Rocket className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-800">FitFinder</span>
            </div>
          </div>

          <Card className="shadow-xl border-0 bg-white/95 backdrop-blur">
            <CardHeader className="space-y-1 pb-6">
              <CardTitle className="text-2xl font-bold text-gray-800">
                Login
              </CardTitle>
              <CardDescription className="text-gray-600">
                Login to access your dashboard account
              </CardDescription>
            </CardHeader>

            <form onSubmit={handleSubmit}>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-gray-700 font-medium">
                    Email
                  </Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="yourname@mail.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10 border-gray-200 focus:border-blue-600 focus:ring-blue-600"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label
                    htmlFor="password"
                    className="text-gray-700 font-medium"
                  >
                    Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="pl-10 pr-10 border-gray-200 focus:border-blue-600 focus:ring-blue-600"
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-2 top-1/2 transform -translate-y-1/2 h-auto p-1 text-gray-400 hover:text-blue-600"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={
                        showPassword ? "Hide password" : "Show password"
                      }
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center space-x-2">
                    <input
                      id="remember"
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-600"
                    />
                    <label htmlFor="remember" className="text-sm text-gray-600">
                      Remember me
                    </label>
                  </div>
                  <Link
                    to="/landing"
                    className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    Forgot password?
                  </Link>
                </div>
              </CardContent>

              <CardFooter className="flex flex-col space-y-4 pt-2">
                <Button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium h-11 flex items-center justify-center gap-2"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    "Signing in..."
                  ) : (
                    <>
                      <LogIn className="w-4 h-4" />
                      Login
                    </>
                  )}
                </Button>

                <div className="text-center text-sm text-gray-600">
                  Don't have an account?{" "}
                  <Link
                    to="/landing"
                    className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
                  >
                    Sign up
                  </Link>
                </div>

                {/* Social Login Buttons */}
                <div className="flex space-x-3 w-full pt-4">
                  <Button
                    variant="outline"
                    className="flex-1 border-gray-300 hover:bg-gray-100 hover:border-gray-600 hover:text-gray-600 transition-colors duration-300"
                  >
                    <FcGoogle className="w-5 h-5 mr-2" />
                    Google
                  </Button>

                  <Button
                    variant="outline"
                    className="flex-1 border-gray-300 hover:bg-black hover:border-black hover:text-white transition-colors duration-300"
                  >
                    <AiFillApple className="w-5 h-5 mr-2" />
                    Apple
                  </Button>

                  <Button
                    variant="outline"
                    className="flex-1 border-gray-300 hover:bg-blue-700 hover:border-blue-800 hover:text-white transition-colors duration-300"
                  >
                    <FaMicrosoft className="w-5 h-5 mr-2" />
                    Microsoft
                  </Button>
                </div>
              </CardFooter>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Login;
