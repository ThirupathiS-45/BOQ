import React from 'react'
import { ArrowRight, Home, Check, Star, BarChart3, Clock, Users, TrendingUp, Zap, Shield } from 'lucide-react'
import { Button } from '@/components/Button'

interface HomePageProps {
  onGetStarted: () => void
}

export const HomePage: React.FC<HomePageProps> = ({ onGetStarted }): JSX.Element => {

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-emerald-50 to-slate-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-emerald-200/30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 group">
              <div className="w-11 h-11 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center shadow-lg hover:shadow-emerald-500/40 transition-shadow">
                <Home size={26} className="text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-black text-slate-900">ArchAI</h2>
                <p className="text-xs text-emerald-600 font-semibold">Smart Design & Estimation</p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-slate-600 hover:text-slate-900 font-medium transition">Features</a>
              <a href="#how" className="text-slate-600 hover:text-slate-900 font-medium transition">How It Works</a>
              <a href="#pricing" className="text-slate-600 hover:text-slate-900 font-medium transition">Pricing</a>
            </div>
            <button 
              onClick={onGetStarted}
              className="px-6 py-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-emerald-500/30 transition-all"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-[calc(100vh-80px)] flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-7xl w-full mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-50 border border-emerald-200 rounded-full">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-emerald-700 font-semibold text-sm">The Future of Architectural Design</span>
              </div>

              <div className="space-y-4">
                <h1 className="text-5xl md:text-6xl font-black text-slate-900 leading-tight">
                  Design & Estimate Your Building with <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">AI Precision</span>
                </h1>
                <p className="text-xl text-slate-600 leading-relaxed">
                  Transform architectural descriptions into stunning floor plans and detailed cost estimates in seconds. Say goodbye to weeks of manual planning.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Button
                  onClick={onGetStarted}
                  className="px-8 py-4 bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold rounded-lg hover:shadow-lg hover:shadow-emerald-500/40 transition-all flex items-center justify-center gap-2"
                >
                  Start Free Now <ArrowRight size={20} />
                </Button>
                <button className="px-8 py-4 bg-white text-slate-900 font-bold rounded-lg border-2 border-emerald-200 hover:border-emerald-500 hover:bg-emerald-50 transition-all">
                  View Demo
                </button>
              </div>

              {/* Trust Indicators */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-lg border border-emerald-100 shadow-sm hover:shadow-md transition-shadow">
                  <p className="text-2xl font-black text-emerald-600">10K+</p>
                  <p className="text-xs text-slate-600 font-medium mt-1">Projects</p>
                </div>
                <div className="bg-white p-4 rounded-lg border border-emerald-100 shadow-sm hover:shadow-md transition-shadow">
                  <p className="text-2xl font-black text-emerald-600">99.8%</p>
                  <p className="text-xs text-slate-600 font-medium mt-1">Accurate</p>
                </div>
                <div className="bg-white p-4 rounded-lg border border-emerald-100 shadow-sm hover:shadow-md transition-shadow">
                  <p className="text-2xl font-black text-emerald-600">&lt;30s</p>
                  <p className="text-xs text-slate-600 font-medium mt-1">Generation</p>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-3xl blur-3xl opacity-15 animate-pulse"></div>
              <div className="relative bg-white rounded-3xl p-8 border-2 border-emerald-200 shadow-2xl">
                <div className="space-y-5">
                  <div className="h-48 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-2xl flex items-center justify-center border border-emerald-200">
                    <svg className="w-20 h-20 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M3 13.5v3.8c0 .6.4 1.2 1 1.2h1v3.5c0 .8.7 1.5 1.5 1.5S8 22.8 8 22v-3h8v3c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5v-3.5h1c.6 0 1-.6 1-1.2v-3.8M3 11h18V4.6c0-.6-.4-1.2-1-1.2H4c-.6 0-1 .6-1 1.2V11zm6-5.5h1V4h-1v1.5zm4 0h1V4h-1v1.5z"/>
                    </svg>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
                      <p className="text-xs text-emerald-600 font-bold uppercase">Area</p>
                      <p className="text-2xl font-black text-slate-900 mt-1">2,500 sqft</p>
                    </div>
                    <div className="bg-teal-50 border border-teal-200 rounded-xl p-4">
                      <p className="text-xs text-teal-600 font-bold uppercase">Rooms</p>
                      <p className="text-2xl font-black text-slate-900 mt-1">5</p>
                    </div>
                    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
                      <p className="text-xs text-emerald-600 font-bold uppercase">Estimate</p>
                      <p className="text-xl font-black text-slate-900 mt-1">₹75L</p>
                    </div>
                    <div className="bg-teal-50 border border-teal-200 rounded-xl p-4">
                      <p className="text-xs text-teal-600 font-bold uppercase">Time</p>
                      <p className="text-2xl font-black text-slate-900 mt-1">20s</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-slate-900 mb-4">Why Choose ArchAI?</h2>
            <p className="text-lg text-slate-600">Built for architects, engineers, and builders who value time</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="p-6 border-2 border-emerald-200 rounded-2xl hover:shadow-xl transition-shadow bg-gradient-to-br from-emerald-50 to-white">
              <div className="w-12 h-12 bg-emerald-500 rounded-lg flex items-center justify-center mb-4">
                <Clock className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Save 80% Time</h3>
              <p className="text-slate-600">What takes weeks of manual work is done in minutes. Get your estimates instantly.</p>
            </div>

            <div className="p-6 border-2 border-teal-200 rounded-2xl hover:shadow-xl transition-shadow bg-gradient-to-br from-teal-50 to-white">
              <div className="w-12 h-12 bg-teal-500 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Reduce Errors</h3>
              <p className="text-slate-600">AI-powered accuracy eliminates human errors. 99.8% precision in estimates.</p>
            </div>

            <div className="p-6 border-2 border-emerald-200 rounded-2xl hover:shadow-xl transition-shadow bg-gradient-to-br from-emerald-50 to-white">
              <div className="w-12 h-12 bg-emerald-500 rounded-lg flex items-center justify-center mb-4">
                <Zap className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Increase Revenue</h3>
              <p className="text-slate-600">Take on more projects. Process more proposals. Win more bids.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-50 to-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-slate-900 mb-4">Powerful Features</h2>
            <p className="text-lg text-slate-600">Everything you need for professional architectural design</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              { icon: Zap, title: 'Instant Generation', desc: 'Convert descriptions to floor plans in seconds' },
              { icon: BarChart3, title: 'Cost Breakdown', desc: 'Detailed material lists and cost analysis' },
              { icon: Shield, title: 'Quality Tiers', desc: 'Budget, Standard, and Premium options' },
              { icon: Clock, title: 'Fast Turnaround', desc: 'Save weeks of manual planning work' },
              { icon: TrendingUp, title: 'Real-time Updates', desc: 'Dynamic pricing based on location' },
              { icon: Users, title: 'Team Collab', desc: 'Share and collaborate seamlessly' },
            ].map((item, i) => (
              <div key={i} className="p-6 border-2 border-emerald-200/50 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all bg-white group">
                <div className="w-14 h-14 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <item.icon className="text-white" size={28} />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works - 4 Steps */}
      <section id="how" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-slate-900 mb-4">How ArchAI Works</h2>
            <p className="text-lg text-slate-600">4-step process to your complete architectural solution</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
            {[
              { num: '1', title: 'Describe Your Vision', desc: 'Enter your building specifications and requirements' },
              { num: '2', title: 'AI Processing', desc: 'Our AI analyzes and structures your input' },
              { num: '3', title: 'Floor Plan Generation', desc: 'Get a professional floor plan instantly' },
              { num: '4', title: 'Cost Estimation', desc: 'Receive detailed cost breakdowns & BOQ' },
            ].map((step, i) => (
              <div key={i} className="relative">
                <div className="bg-white border-3 border-emerald-500 rounded-2xl p-6 h-full">
                  <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-full flex items-center justify-center text-white text-2xl font-black mb-4">
                    {step.num}
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2">{step.title}</h3>
                  <p className="text-slate-600 text-sm">{step.desc}</p>
                </div>
                {i < 3 && (
                  <div className="hidden md:block absolute top-12 -right-3 w-6 h-1 bg-gradient-to-r from-emerald-500 to-teal-500"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-emerald-50 to-teal-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-slate-900 mb-4">Trusted by Industry Leaders</h2>
            <p className="text-lg text-slate-600">See what professionals say about ArchAI</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              { name: 'Rajesh Kumar', role: 'Architect', company: 'Premier Designs', text: 'ArchAI cut our design time in half. Incredible tool!' },
              { name: 'Priya Singh', role: 'Contractor', company: 'BuildRight Co', text: 'The cost estimation accuracy is unmatched. Game-changing!' },
              { name: 'Amit Patel', role: 'Developer', company: 'Urban Constructions', text: 'Our clients love the instant estimates. Highly recommended!' },
            ].map((testimonial, i) => (
              <div key={i} className="bg-white p-8 rounded-2xl border-2 border-emerald-200 shadow-lg hover:shadow-xl transition-shadow">
                <div className="flex gap-1 mb-4">
                  {[...Array(5)].map((_, j) => (
                    <Star key={j} size={18} className="fill-emerald-500 text-emerald-500" />
                  ))}
                </div>
                <p className="text-slate-700 mb-6 font-medium">&quot;{testimonial.text}&quot;</p>
                <div>
                  <p className="font-bold text-slate-900">{testimonial.name}</p>
                  <p className="text-sm text-slate-600">{testimonial.role} at {testimonial.company}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-slate-900 mb-4">Simple, Transparent Pricing</h2>
            <p className="text-lg text-slate-600">Choose the plan that fits your needs</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                name: 'Starter',
                price: 'Free',
                desc: 'Perfect to get started',
                features: ['5 projects/month', 'Basic floor plans', 'Standard quality', 'Email support'],
              },
              {
                name: 'Professional',
                price: '₹999',
                desc: 'For active practitioners',
                features: ['Unlimited projects', 'All quality tiers', 'Advanced features', 'Priority support', 'API access'],
                highlight: true,
              },
              {
                name: 'Enterprise',
                price: 'Custom',
                desc: 'For large teams',
                features: ['White-label', 'Custom integrations', 'Dedicated support', 'SLA guarantee'],
              },
            ].map((plan, i) => (
              <div
                key={i}
                className={`p-8 rounded-2xl border-2 transition-all ${
                  plan.highlight
                    ? 'border-emerald-500 bg-gradient-to-br from-emerald-50 to-teal-50 shadow-2xl scale-105'
                    : 'border-emerald-200 bg-white hover:shadow-lg'
                }`}
              >
                {plan.highlight && (
                  <div className="inline-block px-3 py-1 bg-emerald-500 text-white text-xs font-bold rounded-full mb-4">
                    MOST POPULAR
                  </div>
                )}
                <h3 className="text-2xl font-black text-slate-900 mb-2">{plan.name}</h3>
                <p className="text-emerald-600 font-bold mb-4">{plan.desc}</p>
                <p className="text-4xl font-black text-slate-900 mb-6">
                  {plan.price}
                  {!plan.price.includes('Free') && !plan.price.includes('Custom') && <span className="text-lg text-slate-600 font-medium">/month</span>}
                </p>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="flex items-center gap-3">
                      <Check size={20} className="text-emerald-500 flex-shrink-0" />
                      <span className="text-slate-700 font-medium">{feature}</span>
                    </li>
                  ))}
                </ul>
                <button
                  onClick={onGetStarted}
                  className={`w-full py-3 rounded-lg font-bold transition-all ${
                    plan.highlight
                      ? 'bg-emerald-500 text-white hover:shadow-lg hover:shadow-emerald-500/40'
                      : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                  }`}
                >
                  Get Started
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-emerald-500 via-emerald-600 to-teal-600">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h2 className="text-5xl font-black text-white leading-tight">Ready to Transform Your Design Process?</h2>
            <p className="text-xl text-white/90">Join thousands of professionals already using ArchAI to create better designs faster.</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <button
              onClick={onGetStarted}
              className="px-10 py-4 bg-white text-emerald-600 font-black rounded-lg hover:shadow-2xl hover:scale-105 transition-all hover:bg-emerald-50"
            >
              Start Your Free Trial Now
            </button>
          </div>
          <p className="text-white/80 text-sm">No credit card required • 7-day free trial • Cancel anytime</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gradient-to-b from-slate-900 to-slate-950 text-slate-300 py-20 px-4 sm:px-6 lg:px-8 border-t border-slate-700/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-8 md:gap-12 mb-16">
            <div className="md:col-span-1">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-lg flex items-center justify-center hover:shadow-lg hover:shadow-emerald-500/50 transition-shadow">
                  <Home size={24} className="text-white" />
                </div>
                <h3 className="text-xl font-black text-white">ArchAI</h3>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">Smart architectural design & cost estimation powered by advanced AI.</p>
              <div className="flex gap-4 mt-6">
                <a href="#" className="w-10 h-10 bg-slate-800 hover:bg-emerald-500 rounded-lg flex items-center justify-center transition-colors" title="Twitter">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2s9 5 20 5a9.5 9.5 0 00-9-5.5c4.75 2.25 10 0 10 0"/></svg>
                </a>
                <a href="#" className="w-10 h-10 bg-slate-800 hover:bg-emerald-500 rounded-lg flex items-center justify-center transition-colors" title="LinkedIn">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
                </a>
              </div>
            </div>
            <div>
              <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Product</h4>
              <ul className="space-y-3 text-sm">
                <li><a href="#features" className="text-slate-400 hover:text-emerald-400 transition duration-200">Features</a></li>
                <li><a href="#how" className="text-slate-400 hover:text-emerald-400 transition duration-200">How It Works</a></li>
                <li><a href="#pricing" className="text-slate-400 hover:text-emerald-400 transition duration-200">Pricing</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">API Docs</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Company</h4>
              <ul className="space-y-3 text-sm">
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">About Us</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Blog</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Careers</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Press</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Support</h4>
              <ul className="space-y-3 text-sm">
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Help Center</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Documentation</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Contact</a></li>
                <li><a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Status</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-700/50 pt-12">
            <div className="flex flex-col md:flex-row justify-between items-center gap-6">
              <p className="text-sm text-slate-500">© 2024 ArchAI. All rights reserved. Made with ❤️ for creators.</p>
              <div className="flex gap-8 text-sm">
                <a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Privacy Policy</a>
                <a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Terms of Service</a>
                <a href="#" className="text-slate-400 hover:text-emerald-400 transition duration-200">Cookie Policy</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
