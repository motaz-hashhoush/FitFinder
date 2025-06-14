import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Link } from "wouter";
import { Rocket, Shield, Zap, Users, ArrowRight } from "lucide-react";

const Landing = () => {
  const features = [
    {
      icon: <Rocket className="h-8 w-8" />,
      title: "High Speed",
      description: "A fast application optimized for high performance",
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Full Security",
      description: "Strong protection for your data and information",
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "Ease of Use",
      description: "A simple and easy-to-use interface",
    },
    {
      icon: <Users className="h-8 w-8" />,
      title: "Professional Team",
      description: "24/7 technical support",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link
              to="/"
              className="flex items-center space-x-2 hover:opacity-80 transition"
            >
              <div className="bg-primary rounded-lg p-2">
                <Rocket className="h-6 w-6 text-primary-foreground" />
              </div>
              <h1 className="text-xl font-bold">FitFinder</h1>
            </Link>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/login">
                <Button>Get Started</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Welcome to Our Platform
            </h1>
            <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
              A comprehensive platform that offers you the best advanced tech
              solutions to grow your business and projects efficiently
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/login">
                <Button size="lg" className="flex items-center gap-2">
                  Get Started
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose Our Platform?
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              We provide you with a set of advanced features to ensure a perfect
              experience
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="text-center hover:shadow-lg transition-shadow"
              >
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    <div className="bg-primary/10 rounded-full p-4 text-primary">
                      {feature.icon}
                    </div>
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <Card className="bg-gradient-to-r from-primary to-primary/80 text-primary-foreground">
            <CardContent className="text-center py-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to get started?
              </h2>
              <p className="text-xl mb-8 opacity-90">
                Join thousands of users who trust our platform
              </p>
              <Link to="/login">
                <Button size="lg" variant="secondary" className="text-primary">
                  Start your journey today
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-4">
        <div className="container mx-auto text-center text-muted-foreground">
          <p>&copy; 2024 MyPlatform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
