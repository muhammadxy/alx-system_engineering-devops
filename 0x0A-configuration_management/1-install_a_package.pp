# This Puppet manifest installs flask

package { 'flask':
  ensure   => '2.1.0',
  provider => 'gem',
}