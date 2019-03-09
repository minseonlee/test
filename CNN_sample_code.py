# -*- coding: utf-8 -*-

# Convolutional Neural Networks(CNNs)�� �̿��� Deep MNIST �з���(Classifier)

# ���� ����Ʈ ���� 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# �ʿ��� ���̺귯������ ����Ʈ
import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None


def deepnn(x):
  """���ڸ� �з��ϱ� ���� Deep Neural Networks �׷����� �����Ѵ�.
  ���ڵ�(Args):
    x: (N_examples, 784) ������ ���� input tensor, 784 �Ϲ����� MNIST �������� �ȼ� �����̴�.
  ���ϰ���(Returns):
    tuple (y, keep_prob). y�� (N_examples, 10)������ ����(0-9) tensor�̴�. 
    keep_prob�� dropout�� ���� scalar placeholder�̴�.
  """
  # Convolutional Neural Netwokrs(CNNs)�� ���� reshape.
  # ������ ����(dimension)�� Ư¡��("features")�� ��Ÿ����.-�� �ڵ忡���� �̹����� grayscale�̶� ������������, RGB �̹������ 3����, RGBA��� 4���� �̹��� �� ���̴�.
  x_image = tf.reshape(x, [-1, 28, 28, 1])

  # ù��° convolutional layer - �ϳ��� grayscale �̹����� 32���� Ư¡��(feature)���� ����(maping)�Ѵ�.
  W_conv1 = weight_variable([5, 5, 1, 32])
  b_conv1 = bias_variable([32])
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Pooling layer - 2X��ŭ downsample�Ѵ�.
  h_pool1 = max_pool_2x2(h_conv1)

  # �ι�° convolutional layer -- 32���� Ư¡��(feature)�� 64���� Ư¡��(feature)�� ����(maping)�Ѵ�.
  W_conv2 = weight_variable([5, 5, 32, 64])
  b_conv2 = bias_variable([64])
  h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

  # �ι�° pooling layer.
  h_pool2 = max_pool_2x2(h_conv2)

  # Fully Connected Layer 1 -- 2���� downsampling ���Ŀ�, �츮�� 28x28 �̹����� 7x7x64 Ư¡��(feature map)�� �ȴ�.
  # �̸� 1024���� Ư¡��� ����(maping)�Ѵ�.
  W_fc1 = weight_variable([7 * 7 * 64, 1024])
  b_fc1 = bias_variable([1024])

  h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout - ���� ���⵵�� ��Ʈ���Ѵ�. Ư¡���� co-adaptation�� �����Ѵ�.
  keep_prob = tf.placeholder(tf.float32)
  h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # 1024���� Ư¡��(feature)�� 10���� Ŭ����-���� 0-9-�� ����(maping)�Ѵ�.
  W_fc2 = weight_variable([1024, 10])
  b_fc2 = bias_variable([10])

  y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
  return y_conv, keep_prob


def conv2d(x, W):
  """conv2d�� full stride�� ���� 2d convolution layer�� ��ȯ(return)�Ѵ�."""
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  """max_pool_2x2�� Ư¡��(feature map)�� 2X��ŭ downsample�Ѵ�."""
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  """weight_variable�� �־��� shape�� ���� weight variable�� �����Ѵ�."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  """bias_variable �־��� shape�� ���� bias variable�� �����Ѵ�."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def main(_):
  # data�� import�Ѵ�.
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # ���� �����Ѵ�.
  x = tf.placeholder(tf.float32, [None, 784])

  # loss�� optimizer�� �����Ѵ�.
  y_ = tf.placeholder(tf.float32, [None, 10])

  # Deep Neural Networks �׷����� �����Ѵ�.
  y_conv, keep_prob = deepnn(x)

  # Cross Entropy�� ����Լ�(loss function)���� �����ϰ�, AdamOptimizer�� �̿��ؼ� ��� �Լ��� �ּ�ȭ�Ѵ�.
  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
  train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
  
  # ��Ȯ���� �����Ѵ�.
  correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(20000):
      batch = mnist.train.next_batch(50)
      # 100 Step���� training �����ͼ¿� ���� ��Ȯ���� ����Ѵ�.
      if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: batch[0], y_: batch[1], keep_prob: 1.0})
        print('step %d, training accuracy %g' % (i, train_accuracy))
      # 50% Ȯ���� Dropout�� �̿��ؼ� �н��� �����Ѵ�.
      train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    # �׽�Ʈ �����Ϳ� ���� ��Ȯ���� ����Ѵ�.
    print('test accuracy %g' % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str,
                      default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)